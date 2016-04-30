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

        trace_size = os.path.getsize(trace_filepath)
        if trace_size == 0:
            print 'Deleting empty trace file...' + instance
            os.remove(trace_filepath)
            continue
        with open(trace_filepath, 'r') as prev_file:
            prev_file.seek(-6, os.SEEK_END)
            ending = prev_file.read(6).strip().split()[-1]
        if ending == 'UNSAT':
            print 'UNSAT ' + trace_filepath
        elif ending == '0':
            print 'SAT   ' + trace_filepath
        elif ending == 'INDET':
            print 'INDET ' + trace_filepath
        else:
            print 'Unfinished? ' + ending + ' ' + trace_filepath

        if os.path.exists(analysis_filepath):
            analysis_size = os.path.getsize(analysis_filepath)
            if analysis_size == 0:
                print 'Deleting empty analysis file...' + analysis_filepath
                os.remove(analysis_filepath)
            else:
                with open(analysis_filepath, 'r') as prev_file:
                    prev_file.seek(-6, os.SEEK_END)
                    ending = prev_file.read(6).strip().split()[-1]
                if ending == '0':
                    print 'UNSAT ' + analysis_filepath
                elif ending == 'SAT':
                    print 'SAT   ' + analysis_filepath
                else:
                    print 'Unfinished analysis? ' + ending + ' ' + analysis_filepath
        else:
            print 'No analysis.' 
            
