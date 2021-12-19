"""
Driver code file
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
import plot

np.seterr(all = 'raise')

def main():
    # Instantiate battery_cell
    battery_cell = BatteryCell(ag.CAPACITY_AMP_HR, ag.INTERNAL_RESISTANCE)
    battery_cell.create_cathode(ag.D_CATHODE, ag.R_CATHODE, 
                                ag.MAX_ION_CONCENTRATION_CATHODE)
    battery_cell.create_anode(ag.D_ANODE, ag.R_ANODE, 
                            ag.MAX_ION_CONCENTRATION_ANODE)

    # Create potential look up tables for cathode and anode
    battery_cell.cathode.create_potential_lookup_tables(rp.cathode_potential_ref_array[ag.args.cathode])
    battery_cell.anode.create_potential_lookup_tables(rp.anode_potential_ref_array[ag.args.anode])
            
    # shorthand
    cathode = battery_cell.cathode
    anode = battery_cell.anode

    # Initialize the cathode
    cathode_initial_c = cathode.concentration_list[28]
    cathode.mesh_initialize(ag.R_CATHODE, ag.N_SEGMENTS, ag.n_timestep, cathode_initial_c)

    # Initialize the anode
    anode_initial_c = anode.concentration_list[6]
    anode.mesh_initialize(ag.R_ANODE, ag.N_SEGMENTS, ag.n_timestep, anode_initial_c)

    endtime = ag.n_timestep
    # Run simulation
    for i in range(0, endtime-1):
        cathode.simulation_step(i, ag.DT)
        anode.simulation_step(i, ag.DT)

    voltage = battery_cell.get_voltage()

    # Plot voltage
    plot.plot_voltage(ag.minutes, voltage)

    # Plot concentrations for both electrodes
    plot.plot_concentration(ag.minutes, cathode, 'Cathode')
    plot.plot_concentration(ag.minutes, anode, 'Anode')

# Run 
main()