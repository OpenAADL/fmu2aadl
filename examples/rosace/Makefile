all: build

build: aircraft_dynamics_fmu.aadl engine_fmu.aadl elevator_fmu.aadl \
	fmi_monocore

run:
	./rosace_posix_fmi_monocore/software/software

aircraft_dynamics_fmu.aadl: FMU/Aircraft_Dynamics.fmu
	fmu2aadl FMU/Aircraft_Dynamics.fmu --period=5 --duration=110

engine_fmu.aadl: FMU/Engine.fmu
	fmu2aadl FMU/Engine.fmu --period=5 --duration=110

elevator_fmu.aadl: FMU/Elevator.fmu
	fmu2aadl FMU/Elevator.fmu --period=5 --duration=110

fmi_monocore:
	ocarina -aadlv2 -y -b -g polyorb_hi_c \
	-r ROSACE::FMI::rosace_posix_fmi.monocore rosace-fmi.aadl

clean:
	rm -rf *~

distclean: clean
	rm -rf rosace_posix_monocore rosace_posix_fmi_monocore *_fmu.aadl \
	*.o *_fmu_wrapper.c fmusdk2.0.3 fmu_wrapper.* fmu_* result.csv \
	userdefined.mk
