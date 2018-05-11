all: aircraft_dynamics_fmu.aadl engine_fmu.aadl elevator_fmu.aadl \
	posix_monocore fmi_monocore

aircraft_dynamics_fmu.aadl: Aircraft_Dynamics_OMC.fmu
	fmu2aadl Aircraft_Dynamics_OMC.fmu --period=10 --duration=110

engine_fmu.aadl: Engine_OMC.fmu
	fmu2aadl Engine_OMC.fmu --period=10 --duration=110

elevator_fmu.aadl: Elevator_OMC.fmu
	fmu2aadl Elevator_OMC.fmu --period=10 --duration=110

posix_monocore:
	ocarina -aadlv2 -y -b -g polyorb_hi_c \
	-r ROSACE::POSIX::rosace_posix.monocore rosace-posix.aadl

fmi_monocore:
	ocarina -aadlv2 -y -b -g polyorb_hi_c \
	-r ROSACE::FMI::rosace_posix_fmi.monocore rosace-fmi.aadl

clean:
	rm -rf *~

distclean: clean
	rm -rf rosace_posix_monocore rosace_posix_fmi_monocore *_fmu.aadl *.o *_fmu_wrapper.c fmusdk2.0.3 fmu fmu_wrapper.* fmu_*
