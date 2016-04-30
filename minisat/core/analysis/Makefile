EXEC      = analyze
DEPDIR    = mtl utils

include $(MROOT)/mtl/template.mk

BENCHDIR = ../../../bench/simple

BENCHMARKS = one two three contradict easy-sat imply-sat sparse-sat 

cleanoutput:
	rm *.trace
	rm *.analysis
	rm *.decisions

clean: cleanoutput

%-original.trace: d $(BENCHDIR)/%.cnf
	-../minisat_debug -verb=0 $(word 2,$^) $@

%.analysis: %-original.trace
	./analyze_debug $< $@

%.decisions: %.analysis

%-oracle.trace: %.decisions
	-../minisat_debug -verb=0 -decisions=$^ $@

%-oracle-diff: %-original.trace %-oracle.trace
	-diff $^



run-simple: $(addsuffix -original.trace, $(BENCHMARKS)) 

analyze-simple: $(addsuffix .analysis, $(BENCHMARKS))

feedback-simple: $(addsuffix .oracle-diff, $(BENCHMARKS))
