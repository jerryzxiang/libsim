'''
Electrode 
'''
import numpy as np
import math
import scipy.interpolate

import solver
from mesh import Mesh1D_SPM as Mesh1D_SPM
import arguments as ag

class Electrode():
    '''
    Electrode class
    Contains several variables:
    diffusivity [m$^{2}$ s$^{-1}$],
    particle_radius [m],
    max_ion_concentration [mol m$^{-3}$],
    charge [C], 
    number_moles, 
    volume [m$^{3}$]
    '''
    def __init__(self, diffusivity, particle_radius, max_ion_concentration, charge):
        '''
        Initializes the Electrode class
        '''
        self.diffusivity = diffusivity
        self.particle_radius = particle_radius
        self.max_ion_concentration = max_ion_concentration
        self.charge = charge
        self.number_moles = self.charge / ag.FARADAY_NUMBER
        self.volume = self.number_moles / self.max_ion_concentration
      
        self.potential_history = np.empty([math.ceil(ag.SIMULATION_TIME / ag.DT), 1])
        self.effective_area = self.calculate_effective_area()
    
    def create_potential_lookup_tables(self, ref_list):
        '''
        Creates a potential lookup table based on a reference list
        '''
        self.reference_potential = np.array(ref_list)
        self.concentration_list = np.linspace(0, self.max_ion_concentration, len(ref_list))
        self.potential_interpolator = scipy.interpolate.PchipInterpolator(
            self.concentration_list, self.reference_potential)
    
    def calculate_effective_area(self):
        '''
        Calculates the effective area from the particle radius and 
        particle number, which is calculated from the particle volume:
        $ V_{particle} = \frac{4}{3} \pi R_{particle}^{3} $
        $ N_{particles} = \frac{V}{V_{particle}} $
        $ A_{effective} = N_{particles} * 4 \pi R_{particle}^{2} $
        '''
        particle_volume = (4.0 / 3.0) * math.pi * (self.particle_radius) ** 3
        particle_number = self.volume / particle_volume
        effective_area = particle_number * 4.0 * math.pi * (self.particle_radius ** 2)
        return effective_area
        
    def mesh_initialize(self, length, n_elements, n_timestep, initial_concentration):
        '''
        Initialize mesh
        '''
        self.Mesh = Mesh1D_SPM(n_timestep)
        self.Mesh.add_nodes(length, n_elements, initial_concentration)   

    def electrode_potential(self, node_container):
        '''
        Interpolates concentration values between reference potentials
        and returns a function which is potential as a function of time history
        '''
        potential_function = scipy.interpolate.pchip_interpolate(self.concentration_list, self.reference_potential,
                                                 node_container.concentration[0,:])

        return potential_function

    def set_input_current(self, input_current):
        '''
        Sets input current [A]
        '''
        self.input_current = input_current
    
    def simulation_step(self, timestep_id, dt):
        '''
        Advances the simulation one step 
        '''
        solver.simulation_step(self, timestep_id, dt)