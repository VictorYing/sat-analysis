#!/usr/bin/env python

import os
import subprocess
import sys
import time

start_dir = sys.argv[1]

for dirpath, dirs, files in os.walk(start_dir):
    for filename in files:
        if not filename.endswith('.trace'):
            continue

        trace_filepath = os.path.join(dirpath, filename)
        relpath = os.path.relpath(dirpath, start_dir)
        instance = os.path.join(relpath, filename[:-6])
        instance_filepath = os.path.join(start_dir, instance)
        analysis_filepath = instance_filepath + '.analysis'

        print instance

        trace_size = os.path.getsize(trace_filepath)
        print 'trace size is %d' % trace_size
        if trace_size == 0:
            print 'WARNING!! empty trace file?'
            print 'deleting empty trace file...'
            os.remove(trace_filepath)
            continue 
        if trace_size > 4 * 2**30:
            print 'too large, skipping.'
            continue

        with open(trace_filepath, 'r') as prev_file:
            prev_file.seek(-6, os.SEEK_END)
            line = prev_file.readline()
        if line.rstrip() == 'UNSAT':
            print 'was UNSAT.'
        elif line.strip().split()[-1] == '0':
            print 'was SAT.'
        else:
            print 'not solved. Skipping...'
            continue
        
        if os.path.exists(analysis_filepath):
            print 'skipping as analyzis file already exists.'
            continue
            print 'WARNING! overwriting previous analysis file.'

        start = time.time()
        try:
            code = subprocess.check_call(['./analyze_static',
                                          trace_filepath,
                                          analysis_filepath])
        except:
            print 'Analysis failed!'
            if os.path.getsize(analysis_filepath) == 0:
                print 'deleting empty analysis file...'
                os.remove(analysis_filepath)
        finally:
            print 'analysis took %f seconds' % (time.time() - start)

