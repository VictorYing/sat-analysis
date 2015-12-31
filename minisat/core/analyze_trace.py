#!/usr/bin/env python

import argparse, sys

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

class Branch(Assignment):
    '''Assignment picked by decision heuristic.'''
    def foutput(self, out_file):
        if self.is_needed:
            out_file.write('%i\n' % self.lit)

class Implication(Assignment):
    '''Implied assignment derived from unit propgation.'''
    def __init__(self, lit, antecedent, assignments):
        super(Implication, self).__init__(lit)
        self.antecedent = antecedent
        self.needed_assignments = []
        for lit in antecedent:
            if abs(lit) != self.get_var():
                assn = assignments[abs(lit)]
                assert (lit > 0) != assn.get_val()
                self.needed_assignments.append(assn)
    def needed(self, debug):
        if self.is_needed:
            return
        super(Implication, self).needed(debug)
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
        assert assn.get_var() not in self.assignments
        self.assignments[assn.get_var()] = assn
        self.trail.append(assn)

    def _add_clause(self, clause, cref=''):
        if cref:
            cref = int(cref)
            assert cref not in self.clauses
            self.clauses[int(cref)] = clause

    def _new_decision_level(self):
        self.trail_lim.append(len(self.trail))

    def _backtrack_to(self, level):
        for i in xrange(self.trail_lim[level], len(self.trail)):
            del self.assignments[self.trail[i].get_var()]
        self.trail = self.trail[:self.trail_lim[level]]
        self.trail_lim = self.trail_lim[:level]

    def _analyze_conflict(self, in_file, cref, backtrack_level):
        '''Return True if empty clause has been learned.'''
        conflicting_clause = self.clauses[int(cref)]
        line = in_file.readline()

        if '0\n' == line:
            clause = LearnedClause([], conflicting_clause, self.assignments)
            clause.needed(self.debug)
            return True

        cref, lits = line.split(': ')
        lits = [int(l) for l in lits.split(' ')[:-1]]
        clause = LearnedClause(lits, conflicting_clause, self.assignments)
        self._add_clause(clause, cref)

        self._backtrack_to(int(backtrack_level))

        # Learned clause is asserting
        assn = Implication(clause.get_lits()[0], clause, self.assignments)
        self._add_assignment(assn)

        return False

    def analyze(self, in_file, out_file):
        branch_list = []

        line = in_file.readline()
        while ':' in line:
            cref, lits = line.split(': ')
            lits = [int(l) for l in lits.split(' ')[:-1]]
            self._add_clause(OriginalClause(lits), cref)
            line = in_file.readline()

        while line:
            if 'i' == line[0]:
                # BCP discovered implication
                _, lit, ante = line.split(' ')
                ante = self.clauses[int(ante)]
                assn = Implication(int(lit), ante, self.assignments)
                self._add_assignment(assn)
            elif 'b' == line[0]:
                # Picked branch
                self._new_decision_level()
                branch = Branch(int(line.split(' ')[-1]))
                self._add_assignment(branch)
                branch_list.append(branch)
            elif 'k' == line[0]:
                # Encountered conflict
                _, cref, backtrack_level = line.split(' ')
                if self._analyze_conflict(in_file, cref, backtrack_level):
                    break
            elif 'd' == line[0]:
                cref = int(line.split(' ')[-1])
                del self.clauses[cref]
            else:
                assert False

            if self.debug:
                print self.get_assignments_lits()

            line = in_file.readline()

        for branch in branch_list:
            branch.foutput(out_file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file',
                        help='trace from solver')
    parser.add_argument('output_file',
                        help='necessary branchess')
    parser.add_argument('--debug', action='store_true',
                        help='print information during analysis')
    args = parser.parse_args()

    analyzer = TraceAnalyzer(args.debug)
    with open(args.input_file, 'r') as in_file:
        with open(args.output_file, 'w') as out_file:
            analyzer.analyze(in_file, out_file)

if __name__ == '__main__':
    main()
