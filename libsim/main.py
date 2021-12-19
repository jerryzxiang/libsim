"""
Driver code file: Takes in 5 command line arguments
"""
import numpy as np
import math
import argparse
import scipy.interpolate
import matplotlib.pyplot as plt

from batterycell import BatteryCell as BatteryCell
from mesh import Mesh1D_SPM as Mesh1D_SPM
from derivative import second_derivative
from derivative import first_derivative
import parameters.paramLibrary as pl
import parameters.referencePotentials as rp

np.seterr(all='raise')

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

#Corresponding ion concentrations
#concentration_list_cathode=np.linspace(0, battery_cell.cathode.max_ion_concenctration,33)
#concentration_list_anode=np.linspace(0, battery_cell.anode.max_ion_concenctration,33

# how this would be run in a driver code
battery_cell = BatteryCell(CAPACITY_AMP_HR, INTERNAL_RESISTANCE)
# 
battery_cell.create_cathode(D_CATHODE, R_CATHODE, MAX_ION_CONCENTRATION_CATHODE)
battery_cell.create_anode(D_ANODE, R_ANODE, MAX_ION_CONCENTRATION_ANODE)

#Reference potentials for the electrodes
# Create potential look up tables for cathode and anode
battery_cell.cathode.create_potential_lookup_tables(rp.cathode_potential_ref_array[args.cathode])
battery_cell.anode.create_potential_lookup_tables(rp.anode_potential_ref_array[args.anode])
        
# shorthand
cathode = battery_cell.cathode
anode = battery_cell.anode

# r_cath = np.empty(len(time_history))

# Initialize the cathode
cathode_initial_c = cathode.concentration_list[28]
cathode.mesh_initialize(R_CATHODE, N_SEGMENTS, n_timestep, cathode_initial_c)

# Initialize the anode
anode_initial_c = anode.concentration_list[6]
anode.mesh_initialize(R_ANODE, N_SEGMENTS, n_timestep, anode_initial_c)
second_derivative(cathode.Mesh, 1.0, 1)

A_cathode = cathode.calculate_effective_area()
endtime=n_timestep
for i in range(0, endtime-1):
    cathode.simulation_step(i, DT)


    
#voltage = battery_cell.get_voltage()

# plotting voltage vs time
plt.figure()
plt.plot(cathode.Mesh.node_container[10].concentration[0,:])
plt.show()