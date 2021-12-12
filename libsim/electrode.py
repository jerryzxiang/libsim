#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 16:55:25 2021

@author: antti
"""
import numpy as np
import math
import scipy.interpolate
from .mesh import Mesh1D_SPM as Mesh1D_SPM

from .derivative import second_derivative
from .derivative import first_derivative




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

class Electrode():
    '''
    Electrode class
    Contains several variables:
    diffusivity, particle_radius, max_ion_concentration, charge
    number_moles, volume
    '''
    def __init__(self,diffusivity,particle_radius,max_ion_concentration,charge):
        '''
        Initializes the Electrode class
        '''
        self.diffusivity=diffusivity
        self.particle_radius=particle_radius
        self.max_ion_concentration=max_ion_concentration
        self.charge=charge
        self.number_moles=self.charge/FARADAY_NUMBER
        self.volume=self.number_moles/self.max_ion_concentration
      
        #NEED TO REMOVE MAGIC NUMBERS!!
        self.potential_history=np.empty([math.ceil(SIMULATION_TIME/DT),1])
        #self.effective_area=self.effective_area
        self.effective_area=self.calculate_effective_area()
    
    def create_potential_lookup_tables(self,ref_list):
        '''
        Creates a potential lookup table based on a reference list
        '''
        self.reference_potential=np.array(ref_list)
        #MAGIC NUMBER, NEED REMOVING
        self.concentration_list=np.linspace(0,self.max_ion_concentration,33)
        self.potential_interpolator=scipy.interpolate.PchipInterpolator(
            self.concentration_list, self.reference_potential)
    
    def calculate_effective_area(self):
        '''
        Calculates the effective area from the particle radius and 
        particle number, which is calculated from the particle volume:
        $ V_{particle} = \frac{4}{3} \pi R_{particle}^{3} $
        $ N_{particles} = \frac{V}{V_{particle}} $
        $ A_{effective} = N_{particles} * 4 \pi R_{particle}^{2} $
        '''
        particle_volume=(4.0/3.0)*math.pi*(self.particle_radius)**3
        particle_number=self.volume/particle_volume
        effective_area=particle_number*4.0*math.pi*(self.particle_radius**2)
        return effective_area
        
    def mesh_initialize(self,length,n_elements,n_timestep,initial_concentration):
        '''
        
        '''
        self.Mesh=Mesh1D_SPM(n_timestep)
        self.Mesh.add_nodes(length,n_elements,initial_concentration)

    def electrode_potential(self,concentration_list, potential_ref,
                            concentrations_electrode):
        '''
    
        '''
        potential = np.zeros(len(time_history))
        for i in range(len(time_history)):
            potential[i] = scipy.interpolate.pchip_interpolate(concentration_list, potential_ref, concentrations_electrode[i])
        return potential

    def get_voltage(self,cathode_potential, anode_potential, INPUT_CURRENT, internal_resistance):
        '''
        Returns voltage from input concentration
        '''
        potential_diff = cathode_potential - anode_potential
        internal_potential = INPUT_CURRENT*internal_resistance
        voltage = potential_diff + internal_potential
        return voltage
    
    def set_input_current(self,input_current):
        self.input_current=input_current
    
    def simulation_step(self,timestep_id,dt):
        
        
        arg1=first_derivative(self.Mesh,1.0,timestep_id)
        arg2=second_derivative(self.Mesh,1.0,timestep_id)
        n_nodes=len(arg1)
        for i in range(1,self.Mesh.n_nodes-1):
            node=self.Mesh.node_container[i]
            r=node.x

            r_squared=r**2
            coef1=r_squared
            coef2=r*self.diffusivity/r_squared
            self.Mesh.node_container[i].concentration[0,timestep_id]=(
                self.Mesh.node_container[i].concentration[0,timestep_id-1]+
                dt*(coef1 *arg1[i]+coef2 *arg2[i]))
        
        self.Mesh.node_container[0].concentration[0,timestep_id]=(self.Mesh.
                                                               node_container[1].
                                                               concentration
                                                               [0,timestep_id])
        surface_c=(self.Mesh.dr*(self.input_current)/(self.effective_area*
                                                      self.diffusivity*
                                                      FARADAY_NUMBER)+
            self.Mesh.node_container[n_nodes-2].concentration[0,timestep_id])
        self.Mesh.node_container[n_nodes-1].concentration[0,timestep_id]=surface_c
        self.potential_history[timestep_id]=self.potential_interpolator(surface_c)
    
                                      