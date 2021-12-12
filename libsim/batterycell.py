#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 16:51:57 2021

@author: antti
"""



import numpy as np
import math
import scipy.interpolate
import matplotlib.pyplot as plt

from .electrode import Electrode as Electrode

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




class BatteryCell():
    '''
    BatteryCell model class
    Contains ...
    '''
    def __init__(self,capacity_amp_hour,internal_resistance):
        '''
        Initializes the BatteryCell class
        '''
        self.capacity_amp_hour=capacity_amp_hour
        self.capacity_coulomb=self.capacity_amp_hour*3600.0
        self.internal_resistance=internal_resistance
    def create_cathode(self,diffusivity,particle_radius,max_ion_concentration):
        '''
        Creates cathode containing the following parameters:
        diffusivity, particle_radius, max_ion_concentration
        from the Electrode class
        '''
        self.cathode=Electrode(diffusivity,particle_radius,max_ion_concentration,
                               self.capacity_coulomb)
        self.cathode.input_current=-INPUT_CURRENT
        
    def create_anode(self,diffusivity,particle_radius,max_ion_concentration):
        '''
        Creates anode containing the following parameters:
        diffusivity, particle_radius, max_ion_concentration
        from the Electrode class
        '''
        self.anode=Electrode(diffusivity,particle_radius,max_ion_concentration,
                             self.capacity_coulomb)
        self.anode.input_current=INPUT_CURRENT
        
    def get_voltage(self):
            '''
            Returns voltage from input concentration
            '''
            potential_diff = self.cathode.potential_history - (
                self.anode.potential_history)
            internal_potential = self.anode.input_current*self.internal_resistance
            voltage = potential_diff + internal_potential
            return voltage