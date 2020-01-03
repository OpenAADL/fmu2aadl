help:
	@echo "Available targets"
	@echo " openmodelica_fmu: generate FMU using Modelica"
	@echo " jmodelica_fmu: generate FMU using Modelica"
	@echo " distclean: clean files"

openmodelica_fmu:
	omc script.mos


jmodelica_fmu:
	./MoonLanding.py

clean:
	@-rm -rf *log* *.libs *~ *.makefile

distclean: clean
	@-rm -rf *.fmu
