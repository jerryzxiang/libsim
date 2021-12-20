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
    Contains

    :param capacity_amp_hour: Amp Hour of the system.
    :type capacity_amp_hour: [double]
    :param internal_resistance: Internal resistance of the battery.
    :type internal_resistance: [double]

    '''
    def __init__(self, capacity_amp_hour, internal_resistance):
        '''
        Initializes the BatteryCell class
        '''
        self.capacity_amp_hour = capacity_amp_hour
        self.capacity_coulomb = self.capacity_amp_hour * 3600.0 # time conversion
        self.internal_resistance = internal_resistance

    def create_cathode(self, diffusivity, particle_radius, 
                        max_ion_concentration):
        '''
        Creates cathode containing parameters from the Electrode Class.

        :param diffusivity: Diffusivity desired for the battery model. [(m^2)/s]
        :type diffusivity: [double]
        :param particle_radius: Particle radius of the battery model particles. [m]
        :type particle_radius: [double]
        :param max_ion_concetration: Maximum desired ion concentration. [mol/(m^3)]
        :type max_ion_concentration: [double]
        '''
        self.cathode=Electrode(diffusivity, particle_radius, 
                                max_ion_concentration,
                                self.capacity_coulomb)
        self.cathode.input_current = -ag.INPUT_CURRENT
        
    def create_anode(self, diffusivity, particle_radius, 
                    max_ion_concentration):
        '''
        Creates anode containing parameters from Electrode class.

        :param diffusivity: Diffusivity desired for the battery model. [(m^2)/s]
        :type diffusivity: [double]
        :param particle_radius: Particle radius of the battery model particles. [m]
        :type particle_radius: [double]
        :param max_ion_concetration: Maximum desired ion concentration. [mol/(m^3)]
        :type max_ion_concentration: [double]
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
