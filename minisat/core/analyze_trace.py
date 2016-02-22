#!/usr/bin/env python

import argparse, sys

class Event(object):
    '''Base class for heuristic decisions.'''
    def get_needed(self):
        raise NotImplementedError
    def __str__(self):
        raise NotImplementedError

class Assignment(object):
    '''Base class for variable assignments'''
    def __init__(self, lit):
        self.lit = lit
        self.is_needed = False
    def get_var(self):
        return abs(self.lit)
    def get_val(self):
        return self.lit > 0
    def needed(self, debug):
        if self.is_needed:
            return
        self.is_needed = True
        if debug:
            print 'assignment %i is needed' % self.lit

class Branch(Assignment, Event):
    '''Assignment picked by decision heuristic.'''
    def get_needed(self):
        return self.is_needed
    def __str__(self):
        return "%i\n" % self.lit

class Implication(Assignment):
    '''Implied assignment derived from unit propgation.'''
    def __init__(self, lit, antecedent=None, assignments=None):
        super(Implication, self).__init__(lit)
        self.antecedent = antecedent
        self.needed_assignments = []
        if antecedent:
            for lit in antecedent:
                if abs(lit) != self.get_var():
                    assn = assignments[abs(lit)]
                    assert (lit > 0) != assn.get_val()
                    self.needed_assignments.append(assn)
    def needed(self, debug):
        if self.is_needed:
            return
        super(Implication, self).needed(debug)
        if self.antecedent:
            self.antecedent.needed(debug)
        for assn in self.needed_assignments:
            assn.needed(debug)

class Clause(object):
    '''Base class for clauses.'''
    def __init__(self, lits):
        self.lits = lits
        self.is_needed = False
    def needed(self, debug):
        if self.is_needed:
            return
        self.is_needed = True
        if debug:
            sys.stdout.write('clause ')
            for lit in self.lits:
                sys.stdout.write('%i ' % lit)
            print 'is needed'
    def get_lits(self):
        return self.lits
    def __iter__(self):
        return self.lits.__iter__()

class OriginalClause(Clause):
    '''Clause that was part of the instance.'''
    pass

class LearnedClause(Clause):
    '''Clause derived during conflict analysis.'''
    def __init__(self, lits, conflicting_clause, assignments):
        super(LearnedClause, self).__init__(lits)
        self.needed_assignments = []
        self.antecedent = conflicting_clause
        for lit in conflicting_clause:
            self.needed_assignments.append(assignments[abs(lit)])
    def needed(self, debug):
        if self.is_needed:
            return
        super(LearnedClause, self).needed(debug)
        self.antecedent.needed(debug)
        for assn in self.needed_assignments:
            assn.needed(debug)

class Reset(Event):
    '''A solver reset'''
    def get_needed(self):
        return True
    def __str__(self):
        return 'r\n'

class Deletion(Event):
    '''The deletion of a clause.'''
    def __init__(self, lits):
        self.lits = lits
    def get_needed(self):
        return True
    def __str__(self):
        return 'd ' + ' '.join(str(lit) for lit in self.lits) + ' 0\n'

class TraceAnalyzer(object):
    def __init__(self, debug):
        self.clauses = {}
        self.assignments = {}
        self.trail = []
        self.trail_lim = []
        self.debug = debug

    def get_assignments_lits(self):
        ret = {}
        for i in self.assignments:
            ret[i] = self.assignments[i].lit
        return ret

    def _add_assignment(self, assn):
        if assn.get_var() in self.assignments:
            print 'Variable %i already assigned!' % assn.get_var()
            assert False
        self.assignments[assn.get_var()] = assn
        self.trail.append(assn)

    def _add_clause(self, clause, cref=''):
        if cref:
            cref = int(cref)
            assert cref not in self.clauses
            self.clauses[int(cref)] = clause

    def _decision_level(self):
        return len(self.trail_lim)

    def _new_decision_level(self):
        self.trail_lim.append(len(self.trail))

    def _backtrack_to(self, level):
        assert level < self._decision_level()
        for i in xrange(self.trail_lim[level], len(self.trail)):
            del self.assignments[self.trail[i].get_var()]
        self.trail = self.trail[:self.trail_lim[level]]
        self.trail_lim = self.trail_lim[:level]

    def _analyze_conflict(self, in_file, cref, backtrack_level):
        '''Return True if empty clause has been learned.'''
        conflicting_clause = self.clauses[int(cref)]
        backtrack_level = int(backtrack_level)

        if -1 == backtrack_level:
            clause = LearnedClause([], conflicting_clause, self.assignments)
            clause.needed(self.debug)
            return True

        cref, lits = in_file.readline().split(': ')
        lits = [int(l) for l in lits.split(' ')[:-1]]
        clause = LearnedClause(lits, conflicting_clause, self.assignments)
        self._add_clause(clause, cref)

        self._backtrack_to(backtrack_level)

        # Learned clause is asserting
        assn = Implication(clause.get_lits()[0], clause, self.assignments)
        self._add_assignment(assn)

        return False

    def _analyze_implication(self, line):
        i, lit, ante = line.split(' ')
        assert 'i' == i
        ante = self.clauses[int(ante)]
        assn = Implication(int(lit), ante, self.assignments)
        self._add_assignment(assn)

    def analyze(self, in_file, out_file):
        event_list = []

        line = in_file.readline()
        while ':' in line or 'i' == line[0]:
            if ':' in line:
                cref, lits = line.split(': ')
                lits = [int(l) for l in lits.split(' ')[:-1]]
                self._add_clause(OriginalClause(lits), cref)
                if 0 == len(lits):
                    return
                elif 1 == len(lits):
                    self._add_assignment(Implication(lits[0]))
            elif 'i' == line[0]:
                self._analyze_implication(line)
            else:
                assert False
            line = in_file.readline()

        while 'd' in line:
            cref = int(line.split(' ')[-1])
            del self.clauses[cref]
            line = in_file.readline()

        no_new_line = False
        while line:
            if 'i' == line[0]:
                self._analyze_implication(line)
                num_implications += 1
            elif 'b' == line[0]:
                if last_branch is not None:
                    last_branch.implications = num_implications
                    num_implications = 0
                # Picked branch
                self._new_decision_level()
                branch = Branch(int(line.split(' ')[-1]))
                self._add_assignment(branch)
                event_list.append(branch)
                last_branch = branch
            elif 'k' == line[0]:
                # Encountered conflict
                _, cref, backtrack_level = line.split(' ')
                if self._analyze_conflict(in_file, cref, backtrack_level):
                    break
            elif 'd' == line[0]:
                cref = int(line.split(' ')[-1])
                lits = self.clauses[cref].get_lits()
                del self.clauses[cref]
                event_list.append(Deletion(lits))
            elif 'r' == line[0]:
                if self._decision_level() > 0:
                    self._backtrack_to(0)
                    event_list.append(Reset())
            elif 'm' == line[0]:
                new_clauses = {}
                while 'm' == line[0]:
                    _, old_cref, new_cref = line.split(' ')
                    new_clauses[int(new_cref)] = self.clauses[int(old_cref)]
                    line = in_file.readline()
                self.clauses = new_clauses
                no_new_line = True
            else:
                print line
                assert False

            if self.debug:
                print self.get_assignments_lits()

            if no_new_line:
                no_new_line = False
            else:
                line = in_file.readline()

        if last_branch is not None:
            last_branch.implications = num_implications
            num_implications = 0
        useful_branches = 0
        unuseful_branches = 0
        useful_branch_implications = 0
        unuseful_branch_implications = 0
        for event in event_list:
            if event.get_needed():
                out_file.write(str(event))
                if type(event) is Branch:
                    useful_branches += 1
                    useful_branch_implications += event.implications
            elif type(event) is Branch:
                unuseful_branches += 1
                unuseful_branch_implications += event.implications

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file',
                        help='trace from solver')
    parser.add_argument('output_file',
                        help='necessary decisions')
    parser.add_argument('--debug', action='store_true',
                        help='print information during analysis')
    args = parser.parse_args()

    analyzer = TraceAnalyzer(args.debug)
    with open(args.input_file, 'r') as in_file:
        with open(args.output_file, 'w') as out_file:
            analyzer.analyze(in_file, out_file)

if __name__ == '__main__':
    main()
