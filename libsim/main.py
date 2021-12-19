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
from paramLibrary import immutableCathodeDict
from paramLibrary import immutableAnodeDict

np.seterr(all='raise')

# constant
FARADAY_NUMBER = 9.64853399e4

'''
Argument parsing.
'''
parser = argparse.ArgumentParser()
parser.add_argument('cathode', type = str, 
                    help = 'The first command line arg \
                    is the cathode type: LFP, LCO, NMC')
parser.add_argument('anode', type = str,
                    help = 
                    'The second command line arg \
                    is the anode type: graphite')
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

# input current to the model
INPUT_CURRENT = args.input_current
# input nominal capacity [Ah] to the model, dependent on cell type
CAPACITY_AMP_HR = args.capacity
# internal resistance
INTERNAL_RESISTANCE = args.internal_resistance

# number of radial segments
N_SEGMENTS = 10

# Solid diffusivity in anode
D_ANODE = 8.275e-14
#D_ANODE = immutableAnodeDict.getParams

# particle radius in the anode [meters]
R_ANODE = 3.6e-6

# Solid diffusivity in cathode
D_CATHODE = 1.736e-14

# particle radius in the cathode [meters]
R_CATHODE = 1.637e-7

MAX_ION_CONCENTRATION_CATHODE = 1.035e4

MAX_ION_CONCENTRATION_ANODE = 2.948e4

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
cathode_potential_ref_array = [5.502, 4.353, 3.683, 3.554, 3.493, 3.4, 
                                      3.377,3.364, 3.363, 3.326,3.324, 3.322, 
                                      3.321, 3.316, 3.313, 3.304, 3.295, 3.293,
                                      3.290,3.279 ,3.264,3.261,3.253, 3.245, 
                                      3.238, 3.225, 3.207, 2.937, 2.855, 2.852,
                                      1.026, -1.12,-1.742]

anode_potential_ref_array = [3.959, 3.4, 1.874, 9.233e-1, 9.074e-1, 
                                    6.693e-1,2.481e-3,1.050e-3,1.025e-3, 8.051e-4,
                                    5.813e-4, 2.567e-4, 2.196e-4, 1.104e-4,
                                    3.133e-6,1.662e-6,9.867e-7, 3.307e-7, 1.57e-7,
                                    9.715e-8, 5.274e-9, 2.459e-9, 7.563e-11,
                                    2.165e-12,1.609e-12, 1.594e-12, 1.109e-12,
                                    4.499e-13, 2.25e-14, 1.335e-14, 1.019e-14,
                                    2.548e-16, 1.654e-16]

# Create potential look up tables for cathode and anode
battery_cell.cathode.create_potential_lookup_tables(cathode_potential_ref_array)
battery_cell.anode.create_potential_lookup_tables(anode_potential_ref_array)
        
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