"""
Driver code file: Takes in 5 command line arguments
"""
import numpy as np
import math
import scipy.interpolate
import matplotlib.pyplot as plt

from batterycell import BatteryCell as BatteryCell
from mesh import Mesh1D_SPM as Mesh1D_SPM
from derivative import second_derivative
from derivative import first_derivative
import parameters.paramLibrary as pl
import parameters.referencePotentials as rp
import arguments as ag

np.seterr(all = 'raise')

#Corresponding ion concentrations
#concentration_list_cathode=np.linspace(0, battery_cell.cathode.max_ion_concenctration,33)
#concentration_list_anode=np.linspace(0, battery_cell.anode.max_ion_concenctration,33

# how this would be run in a driver code
battery_cell = BatteryCell(ag.CAPACITY_AMP_HR, ag.INTERNAL_RESISTANCE)
# 
battery_cell.create_cathode(ag.D_CATHODE, ag.R_CATHODE, 
                            ag.MAX_ION_CONCENTRATION_CATHODE)
battery_cell.create_anode(ag.D_ANODE, ag.R_ANODE, 
                        ag.MAX_ION_CONCENTRATION_ANODE)

#Reference potentials for the electrodes
# Create potential look up tables for cathode and anode
battery_cell.cathode.create_potential_lookup_tables(rp.cathode_potential_ref_array[ag.args.cathode])
battery_cell.anode.create_potential_lookup_tables(rp.anode_potential_ref_array[ag.args.anode])
        
# shorthand
cathode = battery_cell.cathode
anode = battery_cell.anode

# r_cath = np.empty(len(time_history))

# Initialize the cathode
cathode_initial_c = cathode.concentration_list[28]
cathode.mesh_initialize(ag.R_CATHODE, ag.N_SEGMENTS, ag.n_timestep, cathode_initial_c)

# Initialize the anode
anode_initial_c = anode.concentration_list[6]
anode.mesh_initialize(ag.R_ANODE, ag.N_SEGMENTS, ag.n_timestep, anode_initial_c)
second_derivative(cathode.Mesh, 1.0, 1)

A_cathode = cathode.calculate_effective_area()
endtime = ag.n_timestep
for i in range(0, endtime-1):
    cathode.simulation_step(i, ag.DT)


    
#voltage = battery_cell.get_voltage()

# plotting voltage vs time
plt.figure()
plt.plot(cathode.Mesh.node_container[10].concentration[0,:])
plt.show()