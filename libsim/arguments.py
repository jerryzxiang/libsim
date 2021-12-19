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
                    is the anode type: graphite:'
                    + str(list(A_dict.keys()))
                    )
parser.add_argument('input_current', type = float,
                    help = 
                    'The third command line arg \
                    is the input current. Units: Amps')
parser.add_argument('capacity', type = float,
                    help = 
                    'The fourth command line arg \
                    is the capacity. Units: Amp Hours')
parser.add_argument('internal_resistance', type = float,
                    help = 
                    'The fifth command line arg \
                    is the internal resistance. Units: Ohms')        
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

# number of radial segments
N_SEGMENTS = 10

# anode segment length
dR_ANODE = R_CATHODE / N_SEGMENTS

# cathode segment length
dR_CATHODE = R_CATHODE / N_SEGMENTS

# simulation time in [seconds]
SIMULATION_TIME = 10

# change in time [seconds]
DT = 0.001

# number of time steps rounded down to nearest integer
n_timestep = math.ceil(SIMULATION_TIME / DT)

# time history
time_history = np.arange(0, SIMULATION_TIME, DT)