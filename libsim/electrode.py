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
    diffusivity (m^2)/s],
    particle_radius [m],
    max_ion_concentration [mol/(m^3)],
    charge [C], 
    number_moles [mol], 
    volume [m^3]

    '''
    def __init__(self, diffusivity, particle_radius, max_ion_concentration, charge):
        '''
        Initializes the Electrode class
        
        :param diffusivity: Diffusivity desired for the battery model.
        :type diffusivity: [double]
        :param particle_radius: Particle radius of the battery model particles.
        :type particle_radius: [double]
        :param max_ion_concetration: Maximum desired ion concentration.
        :type max_ion_concentration: [double]
        :param charge: Charge of the electrode (positive or negative).
        :type charge: [double]

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
        Creates a potential lookup table based on a reference list.

        :param ref_list: Reference list as base for potential lookup table.
        :type ref_list: [numpy array]
        
        '''
        self.reference_potential = np.array(ref_list)
        self.concentration_list = np.linspace(0, self.max_ion_concentration, len(ref_list))
        self.potential_interpolator = scipy.interpolate.PchipInterpolator(
            self.concentration_list, self.reference_potential)
    
    def calculate_effective_area(self):
        '''
        Calculates the effective area from the particle radius and 
        particle number, which is calculated from the particle volume:
        
        :return: effective area from particle volume [m^3]
        :rtype: [double]
        
        '''
        particle_volume = (4.0 / 3.0) * math.pi * (self.particle_radius) ** 3
        particle_number = self.volume / particle_volume
        effective_area = particle_number * 4.0 * math.pi * (self.particle_radius ** 2)
        return effective_area
        
    def mesh_initialize(self, length, n_elements, n_timestep, initial_concentration):
        '''
        
        Initializes the mesh for numerical calculations.

        :param length: Length of the line segment on which the mesh is generated.
        :type length: [double]
        :param n_elements: Number of elements that the length will be split into.
        :type n_elements: [int]
        :param n_timestep: Number of timesteps to be analyzed.
        :type n_timestep: [int]
        :param initial_concentration: Initial concentration of nodes.
        :type initial_concentration: [double]

        '''
        self.Mesh = Mesh1D_SPM(n_timestep)
        self.Mesh.add_nodes(length, n_elements, initial_concentration)   

    def electrode_potential(self, node_container):
        '''
        Returns potential of the electrode.

        :param node_container: List of node objects.
        :type internal_resistance: [list]
        :return: potential_function
        :rtype: [double]

        '''
        potential_function = scipy.interpolate.pchip_interpolate(self.concentration_list, self.reference_potential,
                                                 node_container.concentration[0,:])

        return potential_function

    def set_input_current(self, input_current):
        '''
        Sets input current

        :param input_current: Input Current set for the electrode. [A]
        :type input_current: [double]

        '''
        self.input_current = input_current
    
    def simulation_step(self, timestep_id, dt):
        '''
        Simulates a step.
        
        :param timestep_id: Index for the timestep of the current derivative.
        :type timestep_id: [int]
        
        '''
        solver.simulation_step(self, timestep_id, dt)