all: build

build: aircraft_dynamics_fmu.aadl engine_fmu.aadl elevator_fmu.aadl \
	posix_monocore fmi_monocore

run:
	./rosace_posix_fmi_monocore/software/software

aircraft_dynamics_fmu.aadl: Aircraft_Dynamics.fmu
	fmu2aadl Aircraft_Dynamics.fmu --period=5 --duration=110

engine_fmu.aadl: Engine.fmu
	fmu2aadl Engine.fmu --period=5 --duration=110

elevator_fmu.aadl: Elevator.fmu
	fmu2aadl Elevator.fmu --period=5 --duration=110

posix_monocore:
	ocarina -aadlv2 -y -b -g polyorb_hi_c \
	-r ROSACE::POSIX::rosace_posix.monocore rosace-posix.aadl

fmi_monocore:
	ocarina -aadlv2 -y -b -g polyorb_hi_c \
	-r ROSACE::FMI::rosace_posix_fmi.monocore rosace-fmi.aadl

clean:
	rm -rf *~

distclean: clean
	rm -rf rosace_posix_monocore rosace_posix_fmi_monocore *_fmu.aadl *.o *_fmu_wrapper.c fmusdk2.0.3 fmu fmu_wrapper.* fmu_* result.csv
