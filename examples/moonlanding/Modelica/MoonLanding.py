from pymodelica import compile_fmu
from pyfmi import load_fmu
import pylab as P
import numpy as N

def run_demo():
	print("Compiling Modelica models into FMUs")
	moon_landing_fmu = compile_fmu("MoonLanding","MoonLanding.mo", target='cs', version='2.0',compiler_log_level='d:compilation_moon_landing_log.txt', compiler_options={"cs_solver":1, "cs_step_size":0.001})
	controller_fmu = compile_fmu("Controller_MoonLanding","Controller_MoonLanding.mo", target='cs', version='2.0',compiler_log_level='d:compilation_moon_landing_log.txt', compiler_options={"cs_solver":1, "cs_step_size":0.001})
	
	print("Loading FMUs")
	moonLander = load_fmu(moon_landing_fmu, log_level=7)
	controller = load_fmu(controller_fmu, log_level=7)

	Tstart = 0
	Tend = 100
	moonLander.time = Tstart
	controller.time = Tstart

	print("Instantiation and initialization of experiments")
	moonLander.setup_experiment(start_time = Tstart, stop_time = Tend, stop_time_defined = True)
	moonLander.initialize()
	controller.setup_experiment(start_time = Tstart, stop_time = Tend, stop_time_defined = True)
	controller.initialize()
	print("FMUs initialized")

	moonLander_values_sol = [moonLander.get_variable_valueref('a')] + \
	 [moonLander.get_variable_valueref('v')] + \
	 [moonLander.get_variable_valueref('thrust')]

	moonLander_input_thrust_ref = [moonLander.get_variable_valueref('thrust')]
	moonLander_output_altitude_ref = [moonLander.get_variable_valueref('a')]
	moonLander_output_velocity_ref = [moonLander.get_variable_valueref('v')]

	thrust_ouput_controller_ref = [controller.get_variable_valueref('thrust')]
	
	#Get the initial values for the solution
	t_sol = [Tstart]
	sol = [moonLander.get_real(moonLander_values_sol)]
	
	#Exchange the initial value
	controller_output_thrust = controller.get_real(thrust_ouput_controller_ref)
	moonLander.set_real(moonLander_input_thrust_ref, controller_output_thrust)

	#Setting the time
	time = Tstart
	dt = 0.1 #Step-size

	print("Start of the integration loop")
	
	while time < Tend:

		h = min(dt, Tend-time)

		#Call slaves
		status = controller.do_step(time, h, True)

		controller_output_thrust = controller.get_real(thrust_ouput_controller_ref)
		moonLander.set_real(moonLander_input_thrust_ref, controller_output_thrust)

		status = moonLander.do_step(time,h,True)

		if(status == 'FMI_OK'):
			print("Step accepted by MoonLander FMU")
		
		time = time + h
		t_sol += [time]
		sol += [moonLander.get_real(moonLander_values_sol)]

	P.figure(1)
	P.plot(t_sol, N.array(sol)[:,0])
	P.title(moonLander.get_name())
	P.ylabel('Altitude (m)')
	P.xlabel('Time (s)')
	
	P.figure(2)
	P.plot(t_sol, N.array(sol)[:,1])
	P.title(moonLander.get_name())
	P.ylabel('Velocity (m/s)')
	P.xlabel('Time (s)')

	P.figure(3)
	P.plot(t_sol, N.array(sol)[:,2])
	P.title(moonLander.get_name())
	P.ylabel('Thrust (N)')
	P.xlabel('Time (s)')

	P.show()
			
		
