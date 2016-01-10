#!/usr/bin/env python

import subprocess
import sys

with open(sys.argv[1], 'r') as f:
    while True:
        x = f.readline().rstrip()
        if not x:
            break
        print x
        with open(x + '.log', 'w') as g:
            code = subprocess.call(['../minisat_debug',
                                    '-verb=2',
                                    '../../../bench/sr15bench/' + x + '.cnf',
                                    x + '.trace'],
                                   stdout=g)
        assert 20 == code
        with open(x + '.analysis', 'w') as g:
            subprocess.check_call(['../analyze_trace.py',
                                   x + '.trace',
                                   x + '.decisions'],
                                  stdout=g)

