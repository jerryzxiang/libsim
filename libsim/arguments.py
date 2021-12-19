'''
This file contains the arguments which are parsed
from the command line. There are a total of 8
command line arguments, which are described below.
Additionally, the variable Faraday number is 
declared and initialized here.
'''
import numpy as np
import math
import argparse
import parameters.paramLibrary as pl
import parameters.referencePotentials as rp

# constant
FARADAY_NUMBER = 9.64853399e4

# Getting cathode and anode dict 
C_dict = pl.cathodeDict
A_dict = pl.anodeDict

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('cathode', type = str, 
                    help = 'The first command line arg \
                    is the cathode type:' 
                    + str(list(C_dict.keys()))
                    )
parser.add_argument('anode', type = str,
                    help = 
                    'The second command line arg \
                    is the anode type:'
                    + str(list(A_dict.keys()))
                    )
parser.add_argument('input_current', type = float,
                    help = 
                    'The third command line arg \
                    is the input current. Units: Amps.')
parser.add_argument('capacity', type = float,
                    help = 
                    'The fourth command line arg \
                    is the capacity. Units: Amp Hours.')
parser.add_argument('internal_resistance', type = float,
                    help = 
                    'The fifth command line arg \
                    is the internal resistance. Units: Ohms.')  
parser.add_argument('N_segments', type = int,
                    help = 
                    'The sixth command line arg is the number \
                    of radial segments N. The more radial segments, \
                    the more accurate the simulation is. \"Default\" \
                    value is 10.')
parser.add_argument('simulation_time', type = int,
                    help = 
                    'The seventh command line arg is the simulation \
                    time. Units: Seconds.'
                    ) 
parser.add_argument('dt', type = float,
                    help = 
                    'The eighth command line arg is the time step. \
                    Units: Seconds.'
                    ) 
args = parser.parse_args()


# assigning values based on command line args
D_CATHODE = C_dict[args.cathode][0]
R_CATHODE = C_dict[args.cathode][1]
MAX_ION_CONCENTRATION_CATHODE = C_dict[args.cathode][2]

D_ANODE = A_dict[args.anode][0]
R_ANODE = A_dict[args.anode][1]
MAX_ION_CONCENTRATION_ANODE = A_dict[args.anode][2]

INPUT_CURRENT = args.input_current
CAPACITY_AMP_HR = args.capacity
INTERNAL_RESISTANCE = args.internal_resistance
N_SEGMENTS = args.N_segments
SIMULATION_TIME = args.simulation_time
DT = args.dt

# cathode segment length
dR_CATHODE = R_CATHODE / N_SEGMENTS
# anode segment length
dR_ANODE = R_CATHODE / N_SEGMENTS

# number of time steps rounded down to nearest integer
n_timestep = math.ceil(SIMULATION_TIME / DT)

# time history
time_history = np.arange(0, SIMULATION_TIME, DT)

# time increment in minutes
minutes = np.linspace(0, SIMULATION_TIME / 60, len(time_history))