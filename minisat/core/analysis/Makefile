EXEC      = analyze
DEPDIR    = mtl utils

include $(MROOT)/mtl/template.mk

BENCHDIR = ../../../bench

cleanoutput:
	rm *.trace
	rm *.analysis
	rm *.decisions

clean: cleanoutput

%-original.trace: d
	-../minisat_debug -verb=0 $(word 2,$^) $@

%.analysis: %-original.trace
	./analyze_debug $< $@

%.decisions: %.analysis

%-oracle.trace: %.decisions
	-../minisat_debug -verb=0 -decisions=$^ $@

%-oracle-diff: %-original.trace %-oracle.trace
	-diff $^

one-original.trace: $(BENCHDIR)/simple/one.cnf
two-original.trace: $(BENCHDIR)/simple/two.cnf
three-original.trace: $(BENCHDIR)/simple/three.cnf

one-oracle.trace: $(BENCHDIR)/simple/one.cnf/simple/three.cnf

one-oracle.trace: $(BENCHDIR)/simple/one.cnf
two-oracle.trace: $(BENCHDIR)/simple/two.cnf
three-oracle.trace: $(BENCHDIR)/simple/three.cnf

run-simple: one.trace two.trace three.trace

analyze-simple: one.analysis two.analysis three.analysis

feedback-simple: one-oracle-diff two-oracle-diff three-oracle-diff
