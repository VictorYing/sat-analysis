#!/usr/bin/env python

import os
import subprocess
import sys
import time

input_dir = sys.argv[1]
output_dir = sys.argv[2]

sat_instances = set()
if os.path.exists(sys.argv[3]):
    with open(sys.argv[3], 'r') as f:
        for line in f:
            sat_instances.add(line.strip())
sat_instances_file = open(sys.argv[3], 'a')

solved_instances = set()
if os.path.exists(sys.argv[4]):
    with open(sys.argv[4], 'r') as f:
        for line in f:
            solved_instances.add(line.strip())
solved_instances_file = open(sys.argv[4], 'a')

for dirpath, dirs, files in os.walk(input_dir):
    for filename in files:
        if '.' == filename[0]:
            print 'WARNING! skipping hidden file: ' + filename
            continue
        if '.cnf' != filename[-4:] and '.dimacs' != filename[-7:]:
            print 'WARNING! %s is not an instance?' % filename
            continue

        relpath = os.path.relpath(dirpath, input_dir)
        instance = os.path.join(relpath, filename)
        instance_filepath = os.path.join(dirpath, filename)

        if instance in sat_instances:
            print instance + ' Was already SAT.'
            continue

        if instance in solved_instances:
            print instance + ' was already solved.'
            continue

        print instance

        output_subdir = os.path.join(output_dir, relpath)
        output_filepath = os.path.join(output_dir, instance + '.trace')
        log_filepath = os.path.join(output_dir, instance + '.log')

        if os.path.exists(output_filepath):
            with open(output_filepath, 'r') as prev_file:
                prev_file.seek(-6, os.SEEK_END)
                line = prev_file.readline()
            if line.rstrip() == 'UNSAT':
                print 'WARNING! already solved. Skipping...'
                continue
            else:
                print 'WARNING! overwriting previous trace file.'
        elif not os.path.isdir(output_subdir):
            os.makedirs(output_subdir)

        start = time.time()
        with open(log_filepath, 'w') as g:
            code = subprocess.call(['../minisat_static',
                                    '-verb=2',
                                    '-cpu-lim=1800',
                                    instance_filepath,
                                    output_filepath],
                                   stdout=g)
        print 'run took %f seconds' % (time.time() - start)
        if 10 == code:
            print 'run returned SAT!'
            sat_instances_file.write(instance + '\n')
        if 20 == code:
            solved_instances_file.write(instance + '\n')
        if 20 != code:
            print 'run did not return UNSAT'
            os.remove(os.path.join(output_dir, instance + '.trace'))
            continue
#        start = time.time()
#        with open(x + '.analysis', 'w') as g:
#            subprocess.check_call(['../analyze_trace.py',
#                                   output_dir + x + '.trace',
#                                   output_dir + x + '.decisions'],
#                                  stdout=g)
#        print 'analysis took %f seconds' % (time.time() - start)

