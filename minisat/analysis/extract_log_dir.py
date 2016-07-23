#!/usr/bin/env python

import os
import re
import subprocess
import sys

start_dir = sys.argv[1]

for dirpath, dirs, files in os.walk(start_dir):
    for filename in files:
        if not filename.endswith('.log'):
            continue

        relpath = os.path.relpath(dirpath, start_dir)
        instance = os.path.join(relpath, filename[:-4])
        instance_filepath = os.path.join(start_dir, instance)
        log_filepath = os.path.join(dirpath, filename)
        count_filepath = instance_filepath + '.count'
        print instance

        if os.path.exists(count_filepath):
            count_size = os.path.getsize(count_filepath)
            if count_size == 0:
                print 'deleting empty count file.'
                os.remove(count_filepath)
                continue
        else:
            print 'skipping as count file does not exists.'
            continue

        with open(count_filepath, 'r') as count:
            line = count.readline()

        if line.count(',') < 10:
            print 'WARNING!! count file missing data?'
            print 'skipping...'
            continue
        if line.count(',') >= 19:
            print 'skipping as already includes extra data'
            continue
        if line.count(',') != 10:
            print 'WARNING!! count file has weird data?'
            print 'skipping...'
            continue

        with open(log_filepath, 'r') as log:
            for line in log:
                match = re.search(r'Number of variables: *(\d+)', line)
                if match:
                    variables = int(match.group(1))
                    continue
                match = re.search(r'Number of clauses: *(\d+)', line)
                if match:
                    clauses = int(match.group(1))
                    continue
                match = re.search(r'^restarts *: (\d+)', line)
                if match:
                    restarts = int(match.group(1))
                    continue
                match = re.search(r'^conflicts *: (\d+)', line)
                if match:
                    conflicts = int(match.group(1))
                    continue
                match = re.search(r'^decisions *: (\d+)', line)
                if match:
                    decisions = int(match.group(1))
                    continue
                match = re.search(r'propagations *: (\d+)', line)
                if match:
                    propagations = int(match.group(1))
                    continue
                match = re.search(r'^conflict literals *: (\d+)', line)
                if match:
                    conflict_literals = int(match.group(1))
                    continue
                match = re.search(r'^Memory used *: (.*B)', line)
                if match:
                    memory_used = match.group(1)
                    continue
                match = re.search(r'^CPU time *: (.+) s', line)
                if match:
                    cpu_time = match.group(1)
                    continue
                
        with open(count_filepath, 'a') as count:
            count.write(','.join(str(x) for x in ['',
                                                  variables,
                                                  clauses,
                                                  restarts,
                                                  conflicts,
                                                  decisions,
                                                  propagations,
                                                  conflict_literals,
                                                  memory_used,
                                                  cpu_time]))
