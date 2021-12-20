"""
Driver code file
"""
import numpy as np
import math
import matplotlib.pyplot as plt

from batterycell import BatteryCell as BatteryCell
from electrode import Electrode
from solver import calculate_surface_concentration
from mesh import Mesh1D_SPM as Mesh1D_SPM
from derivative import second_derivative
from derivative import first_derivative
import parameters.paramLibrary as pl
import parameters.referencePotentials as rp
import arguments as ag
import plot

np.seterr(all = 'warn')

def main():
    # Instantiate battery_cell
    battery_cell = BatteryCell(ag.CAPACITY_AMP_HR, ag.INTERNAL_RESISTANCE)
    battery_cell.create_cathode(ag.D_CATHODE, ag.R_CATHODE, 
                                ag.MAX_ION_CONCENTRATION_CATHODE)
    battery_cell.create_anode(ag.D_ANODE, ag.R_ANODE, 
                            ag.MAX_ION_CONCENTRATION_ANODE)

    # shorthand
    cathode = battery_cell.cathode
    anode = battery_cell.anode

    # Create potential look up tables for cathode and anode
    cathode_potential_ref = rp.cathode_potential_ref_array[ag.args.cathode]
    anode_potential_ref = rp.anode_potential_ref_array[ag.args.anode]
    cathode.create_potential_lookup_tables(cathode_potential_ref)
    anode.create_potential_lookup_tables(anode_potential_ref)
    
    # Initialize the cathode
    cathode_initial_c = cathode.concentration_list[math.floor(ag.C_INDEX *
                                    len(rp.cathode_potential_ref_array))]
    cathode.mesh_initialize(ag.R_CATHODE, ag.N_SEGMENTS, 
                            ag.n_timestep, cathode_initial_c)

    # Initialize the anode
    anode_initial_c = anode.concentration_list[math.floor(ag.A_INDEX *
                                    len(rp.anode_potential_ref_array))]
    anode.mesh_initialize(ag.R_ANODE, ag.N_SEGMENTS, 
                        ag.n_timestep, anode_initial_c)

    # Run simulation
    for i in range(0, ag.n_timestep - 1):
        cathode.simulation_step(i, ag.DT)
        anode.simulation_step(i, ag.DT)

    cathode_potential = cathode.electrode_potential(cathode.Mesh.node_container[ag.N_SEGMENTS])
    anode_potential = anode.electrode_potential(anode.Mesh.node_container[ag.N_SEGMENTS])
    voltage = battery_cell.get_voltage(cathode_potential, anode_potential, 
                                    ag.INPUT_CURRENT, ag.INTERNAL_RESISTANCE)
    
    # Plot electrode potential vs time
    plot.plot_voltage(cathode_potential,ag.minutes,
                        'Reference Potential vs Time - Cathode - ' 
                        + str(ag.args.cathode))
    plot.plot_voltage(anode_potential,ag.minutes,
                    'Reference Potential vs Time - Anode - '
                    + str(ag.args.anode))                    
    # Plot battery voltage vs time  
    plot.plot_voltage(voltage, ag.minutes,
                        'Battery Voltage vs. Time (Charging) - ' 
                        + str(ag.args.cathode) + '/' 
                        + str(ag.args.anode))

    # Plot concentrations for both electrodes
    plot.plot_concentration(cathode, cathode_potential, 'Cathode')
    plot.plot_concentration(anode, anode_potential, 'Anode')

# Run 
main()