EXEC      = minisat
DEPDIR    = mtl utils

include $(MROOT)/mtl/template.mk

cleanoutput:
	rm *.trace
	rm *.decisions

clean: cleanoutput

%.trace: d
	-./minisat_debug -verb=0 $(word 2,$^) $@

%.decisions: %.trace
	./analyze_trace.py $< $@

%-oracle.trace: %.decisions
	-./minisat_debug -verb=0 -decisions=$^ $@

%-oracle-diff: %.trace %-oracle.trace
	-diff $^

one.trace: ../../bench/simple/one.cnf
two.trace: ../../bench/simple/two.cnf
three.trace: ../../bench/simple/three.cnf

one-oracle.trace: ../../bench/simple/one.cnf
two-oracle.trace: ../../bench/simple/two.cnf
three-oracle.trace: ../../bench/simple/three.cnf

run-simple: one.trace two.trace three.trace

analyze-simple: one.decisions two.decisions three.decisions

feedback-simple: one-oracle-diff two-oracle-diff three-oracle-diff
