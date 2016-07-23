#!/usr/bin/env python

import os
import subprocess
import sys

start_dir = sys.argv[1]

for dirpath, dirs, files in os.walk(start_dir):
    for filename in files:
        if not filename.endswith('.analysis'):
            continue

        relpath = os.path.relpath(dirpath, start_dir)
        instance = os.path.join(relpath, filename[:-9])
        instance_filepath = os.path.join(start_dir, instance)
        analysis_filepath = os.path.join(dirpath, filename)
        count_filepath = instance_filepath + '.count'
        print instance

        if os.path.exists(count_filepath):
            count_size = os.path.getsize(count_filepath)
            if count_size == 0:
                print 'deleting empty count file.'
                os.remove(count_filepath)
            else:
                print 'skipping as count file already exists.'
                continue
                print 'WARNING! overwriting previous count file.'


        analysis_size = os.path.getsize(analysis_filepath)
        print 'analysis size is %d' % analysis_size
        if analysis_size == 0:
            print 'deleting empty analysis file.'
            os.remove(analysis_filepath)
            continue

        with open(analysis_filepath, 'r') as prev_file:
            prev_file.seek(-5, os.SEEK_END)
            ending = prev_file.read(6).strip().split()[-1]
        if ending == '0':
            print 'UNSAT'
        elif ending == 'SAT':
            print 'SAT'
        else:
            print 'Unfinished analysis? ' + ending + ' ' + analysis_filepath
            print 'Skipping...'
            continue

        with open(analysis_filepath, 'r') as prev_file:
            lines = 0
            required = 0
            skippable = 0
            branches = 0
            req_branches = 0
            skip_branches = 0
            props = 0
            req_props = 0
            skip_props = 0
            for line in prev_file:
                if line:
                    lines += 1
                    first_char = line[0]
                    if first_char == '!':
                        required += 1
                        event_type = line[2]
                        if event_type == 'b':
                            req_branches += 1
                            branches += 1
                        elif event_type == 'i':
                            req_props += 1
                            props += 1
                        elif event_type == 'S':
                            break
                    elif first_char == '~' or first_char == '-':
                        skippable += 1
                        if 'b' == line[2]:
                            skip_branches += 1
                            branches += 1
                        elif 'i' == line[2]:
                            skip_props += 1
                            props += 1
                    else:
                        if first_char == 'b':
                            branches += 1
                        if first_char == 'i':
                            props += 1
                else:
                    break
            print lines, 100.0*required/lines, 100.0*skippable/lines

        with open(count_filepath, 'w') as output:
            output.write(','.join(str(x) for x in
                                  [instance,
                                   relpath,
                                   lines,
                                   required,
                                   skippable,
                                   branches,
                                   req_branches,
                                   skip_branches,
                                   props,
                                   req_props,
                                   skip_props]))
        
