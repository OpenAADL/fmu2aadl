all: moonlanding_fmu.aadl check_aadl code_gen build

moonlanding_fmu.aadl: MoonLanding.fmu
	fmu2aadl MoonLanding.fmu --period=10 --duration=110

code_gen: moonlanding_fmu.aadl
	ocarina -aadlv2 -y -g polyorb_hi_c moonlanding.aadl

build:  moonlanding_fmu.aadl
	ocarina -aadlv2 -y -b -g polyorb_hi_c moonlanding.aadl

check_aadl: moonlanding_fmu.aadl
	ocarina -aadlv2 -y moonlanding.aadl

run:
	@./moonlanding_sys_impl/lander/lander

clean:
	-rm -rf *~

distclean: clean
	-rm -rf moonlanding_sys_impl fmu_wrapper.* userdefined.mk	\
	moonlanding_fmu.aadl moonlanding_fmu_wrapper.c result.csv	\
	fmu_* fmu fmusdk2.0.3
