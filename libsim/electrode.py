'''
Electrode 
'''
import numpy as np
import math
import scipy.interpolate

import solver
from mesh import Mesh1D_SPM as Mesh1D_SPM

from derivative import second_derivative
from derivative import first_derivative

# constant
FARADAY_NUMBER = 9.64853399e4

# input current to the model
# input nominal capacity [Ah] to the model
# dependent on cell type. This is for a 26650 cell
# should be parsed as a command line arg
INPUT_CURRENT = 0.5 
CAPACITY_AMP_HR = 2.3
INTERNAL_RESISTANCE = 0.150

# number of radial segments
N_SEGMENTS = 10

# Solid diffusivity in anode
D_ANODE = 8.275e-14

# particle radius in the anode [meters]
R_ANODE = 3.6e-6

# Solid diffusivity in cathode
D_CATHODE = 1.736e-14

# particle radius in the cathode [meters]
R_CATHODE = 1.637e-7

# simulation time in [seconds]
SIMULATION_TIME = 10 

# change in time [seconds]
DT = 0.001

# number of time steps rounded down to nearest integer
n_timestep = math.ceil(SIMULATION_TIME / DT)

# time history
time_history = np.arange(0, SIMULATION_TIME, DT)

class Electrode():
    '''
    Electrode class
    Contains several variables:
    diffusivity, particle_radius, max_ion_concentration, charge
    number_moles, volume
    '''
    def __init__(self, diffusivity, particle_radius, max_ion_concentration, charge):
        '''
        Initializes the Electrode class
        '''
        self.diffusivity = diffusivity
        self.particle_radius = particle_radius
        self.max_ion_concentration = max_ion_concentration
        self.charge = charge
        self.number_moles = self.charge / FARADAY_NUMBER
        self.volume = self.number_moles / self.max_ion_concentration
      
        #NEED TO REMOVE MAGIC NUMBERS!!
        self.potential_history = np.empty([math.ceil(SIMULATION_TIME / DT), 1])
        #self.effective_area=self.effective_area
        self.effective_area = self.calculate_effective_area()
    
    def create_potential_lookup_tables(self, ref_list):
        '''
        Creates a potential lookup table based on a reference list
        '''
        self.reference_potential = np.array(ref_list)
        #MAGIC NUMBER, NEED REMOVING
        self.concentration_list = np.linspace(0, self.max_ion_concentration, 33)
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
        
        '''
        self.Mesh = Mesh1D_SPM(n_timestep)
        self.Mesh.add_nodes(length, n_elements, initial_concentration)

    def electrode_potential(self, concentration_list, potential_ref,
                            concentrations_electrode):
        '''
        Interpolates concentration values between reference potentials
        '''
        potential = np.zeros(len(time_history))
        for i in range(len(time_history)):
            potential[i] = scipy.interpolate.pchip_interpolate(
                concentration_list, potential_ref, concentrations_electrode[i])
        return potential

    def get_voltage(self, cathode_potential, anode_potential, INPUT_CURRENT, internal_resistance):
        '''
        Returns voltage from input concentration
        '''
        potential_diff = cathode_potential - anode_potential
        internal_potential = INPUT_CURRENT * internal_resistance
        voltage = potential_diff + internal_potential
        return voltage
    
    def set_input_current(self, input_current):
        '''
        Sets input current
        '''
        self.input_current = input_current
    
    def simulation_step(self, timestep_id, dt):
        '''
        Advances the simulation one step 
        '''
        solver.simulation_step(self,timestep_id,dt)