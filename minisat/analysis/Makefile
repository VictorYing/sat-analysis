EXEC      = analyze
DEPDIR    = mtl utils

include $(MROOT)/mtl/template.mk

BENCHDIR = ../../bench/simple

BENCHMARKS = one two three contradict easy-sat imply-sat sparse-sat 

cleanoutput:
	rm *.trace
	rm *.csv

clean: cleanoutput

%.trace: $(BENCHDIR)/%.cnf
	-../core/minisat_debug -verb=0 $< $@

%.csv: %.trace d
	./analyze_debug $< $@

run-simple: $(addsuffix .trace, $(BENCHMARKS))

analyze-simple: $(addsuffix .csv, $(BENCHMARKS))
