#!/usr/bin/env python

'''
fmu2aadl: convert .fmu model into an AADL model

Usage:
   fmu2aadl.py <fmu_file> --period=<ms> --duration=<ms>

Options:
  -h --help      Show this screen.
  --version      Show version.
  --period=<ms>  Period of activation of the FMU, in ms
  --duration=<s> Duration of the simulation, in s
'''

################################################################################

from docopt import docopt
import fmu2aadl

def main():
    # Read command line arguments
    args = docopt(__doc__, version='fmu2aadl 0.1')
    fmu_file = args['<fmu_file>']
    period =  args['--period']
    duration = args['--duration']

    fmu2aadl.fmu2aadl(fmu_file, period, duration)
