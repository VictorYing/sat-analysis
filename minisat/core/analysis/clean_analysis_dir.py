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

        print instance

        analysis_size = os.path.getsize(analysis_filepath)
        print 'analysis size is %d' % analysis_size
        if analysis_size == 0:
            print 'deleting empty analysis file.'
            os.remove(analysis_filepath)
            continue

        with open(analysis_filepath, 'r') as prev_file:
            prev_file.seek(-4, os.SEEK_END)
            line = prev_file.readline()
        if line.rstrip() == '! 0':
            print 'Analysis confirmed UNSAT'
            continue
        else:
            raise Exception()
        
