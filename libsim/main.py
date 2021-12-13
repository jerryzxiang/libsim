"""
Main file containing several classes and their definitions

? Should each individual class be split up into its own file ?
"""

import numpy as np
import math
import scipy.interpolate
import matplotlib.pyplot as plt
from batterycell import BatteryCell as BatteryCell
from mesh import Mesh1D_SPM as Mesh1D_SPM
from derivative import second_derivative
from derivative import first_derivative

# constant
FARADAY_NUMBER=9.64853399e4

# input current to the model
# should be parsed as a command line arg
INPUT_CURRENT=0.5 
INTERNAL_RESISTANCE=0.150
# input nominal capacity [Ah] to the model
# should be parsed as a command line arg
# dependent on cell type. This is for a 26650 cell
AMP_HOURS=2.3

# number of radial segments
N_SEGMENTS=10

# particle radius in the anode [meters]
R_ANODE=3.6e-6

D_CATHODE = 1.736e-14

# particle radius in the cathode [meters]
R_CATHODE=1.637e-7

# simulation time in [seconds]
SIMULATION_TIME=10 

# change in time [seconds]
DT=0.001

# number of time steps rounded down to nearest integer
n_timestep=math.ceil(SIMULATION_TIME/DT)
print('n_timestep',n_timestep)

# time history
time_history = np.arange(0, SIMULATION_TIME, DT)
print('time_history',time_history)


#Corresponding ion concentrations
#concentration_list_cathode=np.linspace(0, battery_cell.cathode.max_ion_concenctration,33)
#concentration_list_anode=np.linspace(0, battery_cell.anode.max_ion_concenctration,33

# how this would be run in a driver code
capacity_amp_hour = 2.3
battery_cell=BatteryCell(capacity_amp_hour,INTERNAL_RESISTANCE)
battery_cell.create_cathode(1.736e-14,1.637e-7,1.035e4)
battery_cell.create_anode(8.275e-14,3.600e-6,2.948e4)

#Reference potentials for the electrodes
#cathode_potential_ref = 
cathode_potential_ref_array = [5.502, 4.353, 3.683, 3.554, 3.493, 3.4, 
                                      3.377,3.364, 3.363, 3.326,3.324, 3.322, 
                                      3.321, 3.316, 3.313, 3.304, 3.295, 3.293,
                                      3.290,3.279 ,3.264,3.261,3.253, 3.245, 
                                      3.238, 3.225, 3.207, 2.937, 2.855, 2.852,
                                      1.026, -1.12,-1.742]

battery_cell.cathode.create_potential_lookup_tables(cathode_potential_ref_array)

#anode_potential_ref = 
anode_potential_ref_array = [3.959, 3.4, 1.874, 9.233e-1, 9.074e-1, 
                                    6.693e-1,2.481e-3,1.050e-3,1.025e-3, 8.051e-4,
                                    5.813e-4, 2.567e-4, 2.196e-4, 1.104e-4,
                                    3.133e-6,1.662e-6,9.867e-7, 3.307e-7, 1.57e-7,
                                    9.715e-8, 5.274e-9, 2.459e-9, 7.563e-11,
                                    2.165e-12,1.609e-12, 1.594e-12, 1.109e-12,
                                    4.499e-13, 2.25e-14, 1.335e-14, 1.019e-14,
                                    2.548e-16, 1.654e-16]
battery_cell.anode.create_potential_lookup_tables(anode_potential_ref_array)
        

#shorthand
cathode=battery_cell.cathode
anode=battery_cell.anode

dr_cath = R_CATHODE/N_SEGMENTS
r_cath = np.empty(len(time_history))


#Initialize the cathode
concentrations_cathode = np.zeros((N_SEGMENTS+1,len(time_history)))
#print('length time history',len(time_history))
#print('concentrations_cathode', concentrations_cathode)
concentrations_cathode[:,0] = cathode.concentration_list[28]
#print(concentrations_cathode[0,:])
#print('concentrations_cathode', concentrations_cathode)
cathode_initial_c=cathode.concentration_list[28]
#print(cathode_initial_c)
cathode.mesh_initialize(R_CATHODE, N_SEGMENTS, n_timestep, cathode_initial_c)
#print('cathode.Mesh=',cathode.Mesh.get_concentration_by_id())

anode_initial_c=anode.concentration_list[6]
anode.mesh_initialize(R_ANODE,N_SEGMENTS,n_timestep,anode_initial_c)
second_derivative(cathode.Mesh,1.0,1)

A_cathode = cathode.calculate_effective_area()
print('area cathode', A_cathode)

#for i in range(len(time_history)):
#    r_cath[i]=i*dr_cath

#for i in range(len(time_history)):
#    first_derivative(cathode.Mesh,1.0,i)
#    second_derivative(cathode.Mesh,1.0,i)


print('cathode.concentration_list:', cathode.concentration_list)
print('cathode_initial_c', cathode_initial_c)
print(len(cathode.concentration_list))
print(len(cathode_potential_ref_array))
#cathode_potential = cathode.electrode_potential(cathode.concentration_list, cathode_potential_ref_array, concentration)
#print('cathode_potential', cathode_potential)

#compute the derivatives



#generate the time history:

for i in range(1,n_timestep):
    cathode.simulation_step(i,DT)
    anode.simulation_step(i,DT)
    
    
voltage=battery_cell.get_voltage()