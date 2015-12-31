EXEC      = minisat
DEPDIR    = mtl utils

include $(MROOT)/mtl/template.mk

run-simple: rs
	-./minisat_static -verb=0 ../../bench/simple/three.cnf three.trace
	-./minisat_static -verb=0 ../../bench/simple/two.cnf two.trace

analyze-simple: run-simple
	./analyze_trace.py three.trace three.branch
	./analyze_trace.py two.trace two.branch
