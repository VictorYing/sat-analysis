#!/usr/bin/env python

import os
import subprocess
import sys
import time

output_dir = sys.argv[2]
if output_dir[-1] != '/':
    output_dir += '/'
with open(sys.argv[1], 'r') as f:
    while True:
        x = f.readline().rstrip()
        if not x:
            break
        if '.cnf' == x[-4:]:
            x = x[:-4]
        print x

        if x + '.trace' in os.listdir(output_dir):
            with open(output_dir + x + '.trace', 'r') as prev_file:
                prev_file.seek(-6, os.SEEK_END)
                line = prev_file.readline()
            if line.rstrip() == 'UNSAT':
                print 'already solved'
                continue

        start = time.time()
        with open(x + '.log', 'w') as g:
            code = subprocess.call(['../minisat_static',
                                    '-verb=2',
                                    '-cpu-lim=3600',
                                    '../../../bench/sr15/' + x + '.cnf',
                                    output_dir + x + '.trace'],
                                   stdout=g)
        print 'run took %f seconds' % (time.time() - start)
        if 20 != code:
            print 'run did not return UNSAT'
            os.remove(os.path.join(output_dir, x + '.trace'))
            continue
#        start = time.time()
#        with open(x + '.analysis', 'w') as g:
#            subprocess.check_call(['../analyze_trace.py',
#                                   output_dir + x + '.trace',
#                                   output_dir + x + '.decisions'],
#                                  stdout=g)
#        print 'analysis took %f seconds' % (time.time() - start)

