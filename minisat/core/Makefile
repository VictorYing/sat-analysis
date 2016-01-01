EXEC      = minisat
DEPDIR    = mtl utils

include $(MROOT)/mtl/template.mk

cleantrace:
	-rm one.trace two.trace three.trace
cleandecisions:
	-rm one.decisions two.decisions three.decisions
cleanoutput: cleantrace cleandecisions
clean: cleanoutput

%.trace: rs
	-./minisat_static -verb=0 $(word 2,$^) $@

%.decisions: %.trace
	./analyze_trace.py $< $@

one.trace: ../../bench/simple/one.cnf
two.trace: ../../bench/simple/two.cnf
three.trace: ../../bench/simple/three.cnf

run-simple: one.trace two.trace three.trace

analyze-simple: one.decisions two.decisions three.decisions
