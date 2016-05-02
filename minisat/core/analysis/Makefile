EXEC      = analyze
DEPDIR    = mtl utils

include $(MROOT)/mtl/template.mk

BENCHDIR = ../../../bench/simple

BENCHMARKS = one two three contradict easy-sat imply-sat sparse-sat 

cleanoutput:
	rm *.trace
	rm *.analysis

clean: cleanoutput

%.trace: d $(BENCHDIR)/%.cnf
	-../minisat_debug -verb=0 $(word 2,$^) $@

%.analysis: %.trace
	./analyze_debug $< $@

run-simple: $(addsuffix .trace, $(BENCHMARKS))

analyze-simple: $(addsuffix .analysis, $(BENCHMARKS))
