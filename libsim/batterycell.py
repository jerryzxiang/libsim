'''
BatteryCell
'''
import numpy as np
import matplotlib.pyplot as plt
from electrode import Electrode as Electrode
import arguments as ag

class BatteryCell():
    '''
    BatteryCell model class
    Contains functions to create cathode and anode

    '''
    def __init__(self, capacity_amp_hour, internal_resistance):
        '''
        Initializes the BatteryCell class
        '''
        self.capacity_amp_hour = capacity_amp_hour
        self.capacity_coulomb = self.capacity_amp_hour * 3600.0
        self.internal_resistance = internal_resistance

    def create_cathode(self, diffusivity, particle_radius, 
                        max_ion_concentration):
        '''
        Creates cathode containing the following parameters:
        diffusivity, particle_radius, max_ion_concentration
        from the Electrode class
        '''
        self.cathode=Electrode(diffusivity, particle_radius, max_ion_concentration,
                               self.capacity_coulomb)
        self.cathode.input_current = -ag.INPUT_CURRENT
        
    def create_anode(self, diffusivity, particle_radius, 
                    max_ion_concentration):
        '''
        Creates anode containing the following parameters:
        diffusivity, particle_radius, max_ion_concentration
        from the Electrode class
        '''
        self.anode=Electrode(diffusivity, particle_radius, 
                            max_ion_concentration,
                            self.capacity_coulomb)
        self.anode.input_current = ag.INPUT_CURRENT

    def get_voltage(self, cathode_potential, anode_potential, 
                    INPUT_CURRENT, internal_resistance):
        potential_diff = cathode_potential - anode_potential
        internal_potential = INPUT_CURRENT * internal_resistance
        voltage = potential_diff + internal_potential
        
        return voltage
