from pymodelica import compile_fmu
from pyfmi import load_fmu

def run_demo():
	print("Compiling the FMUs")
	engine_fmu = compile_fmu("Engine","Engine.mo", target='cs', version='2.0');
	elevator_fmu = compile_fmu("Elevator","Elevator.mo", target='cs', version='2.0')
	aircraft_dynamics_fmu = compile_fmu("Aircraft_Dynamics","Aircraft_Dynamics.mo", target='cs', version='2.0')
