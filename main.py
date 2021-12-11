"""
Main file containing several classes and their definitions

? Should each individual class be split up into its own file ?
"""

import numpy as np
import math
import scipy.interpolate
import matplotlib.pyplot as plt
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

# change in time [seconds]
DT=0.001

# number of time steps rounded down to nearest integer
n_timestep=math.ceil(SIMULATION_TIME/DT)
print('n_timestep',n_timestep)

# time history
time_history = np.arange(0, SIMULATION_TIME, DT)
print('time_history',time_history)

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
            self.Mesh.node_container[i].concentration[0,timestep_id]+=dt*(coef1*
                                                arg1[i]+coef2*arg2[i])
        
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
    
                                                              
        

        
#Corresponding ion concentrations
#concentration_list_cathode=np.linspace(0, battery_cell.cathode.max_ion_concenctration,33)
#concentration_list_anode=np.linspace(0, battery_cell.anode.max_ion_concenctration,33


class Node():
    '''
    Node class

    '''
    #Right now the node class is written in a way that the coordinates do not 
    #change, they do not have time history
    def __init__(self,mesh,node_id,x):
        '''
        
        '''
        self.x=np.array(x)
        self.node_id=node_id
        return
    
class Node_SPM(Node):
    '''
    Node_SPM class, subset of Node
    '''
    def __init__(self,mesh,node_id,x,initial_concentration):
        '''
        Initialize Node_SPM class with the
        mesh, node_id, x, initial_concentration
        '''
        #The timehistory
        self.concentration=np.empty((1,mesh.n_timestep))
        self.concentration[0,0]=initial_concentration
        super().__init__(mesh,node_id,x)


class Mesh1D():
    '''
    Mesh1D class
    '''
    #Need to make init empty, while creating mesh it is not really necessary
    #To know the lengths etc. This is better done in some separate generator
    #This way there is flexibility in how the mesh is created.
    def __init__(self,n_timestep):
        '''
        Initialize Mesh1D class with
        n_timestep
        '''
        self.node_id=0
        #Initialize the container (list in this implementation holding the nodes)
        self.node_container=[]
        self.n_timestep=n_timestep
        self.n_nodes=0

    def add_node(self,x):
        '''
        Adds a node based on x location, returns new node
        '''
        self.node_container.append(Node(self,self.node_id,x))
        self.node_id+=1
        self.n_nodes+=1
        return

    def add_nodes(self,length,n_elements):
        '''
        Add nodes of a length with n_elements
        '''
        #helper variables
        self.dr=length/n_elements
        x=0.0
        for i in range(n_elements+1):
            self.add_node(x+i*self.dr)
            
class Mesh1D_SPM(Mesh1D):
    '''
    Mesh1D_SPM class, subset of Mesh1D
    '''
    def add_node(self,x,initial_concentration):
        '''
        Adds a node based on x location, returns new node
        '''
        self.node_container.append(Node_SPM(self,self.node_id,x,initial_concentration))
        self.node_id+=1
        self.n_nodes+=1
        return
    
    def add_nodes(self,length,n_elements,initial_concentration):
        '''
        Add nodes of a length with n_elements
        '''
        #helper variables
        self.dr=length/n_elements
        x=0.0
        for i in range(n_elements+1):
            self.add_node(x+i*self.dr,initial_concentration)
                
    def get_concentration_by_id(self,node_id,timestep):
        '''
        Get concentration at a node, and return
        '''
        return self.node_container[node_id].concentration[0,timestep]
        
        
    

def second_derivative(Mesh,coefficient,timestep):
    '''
    Calculates the second derivative in Fick's Law
    '''
    #The coefficient to be passed is a function
    #Mesh is the mesh for which the derivative is to be evaluated.
    
    second_derivative=np.empty([Mesh.n_nodes,1])
    
    #utilize a "phantom node" to be able to compute the second derivative at 
    #The edges
    for i in range(1,Mesh.n_nodes-1):
        i_plus_1=Mesh.get_concentration_by_id(i+1,timestep)
        i_minus_1=Mesh.get_concentration_by_id(i-1,timestep)
        i_center=Mesh.get_concentration_by_id(i,timestep)
        distance=Mesh.node_container[i+1].x-Mesh.node_container[i].x
        second_derivative[i,0]=(i_plus_1-2*i_center+i_minus_1)/(distance**2)
        second_derivative[i,0]=coefficient*second_derivative[i,0]
    
    return second_derivative
    
def first_derivative(Mesh,coefficient,timestep):  
    '''
    Calculates the first derivative in Fick's Law
    '''
    #The coefficient to be passed is a function
    #Mesh is the mesh for which the derivative is to be evaluated.
    
    
    first_derivative=np.empty([Mesh.n_nodes,1])
        
    #utilize a "phantom node" to be able to compute the second derivative at 
    #The edges
    for i in range(1,Mesh.n_nodes-1):
        i_plus_1=Mesh.get_concentration_by_id(i+1,timestep)
        i_minus_1=Mesh.get_concentration_by_id(i-1,timestep)
        distance=Mesh.node_container[i+1].x-Mesh.node_container[i].x
        first_derivative[i,0]=(i_plus_1-i_minus_1)/(distance)
        first_derivative[i,0]=coefficient*first_derivative[i,0]
        
    return first_derivative
        
    



        




# how this would be run in a driver code
capacity_amp_hour = 2.3
battery_cell=BatteryCell(capacity_amp_hour,INTERNAL_RESISTANCE)
battery_cell.create_cathode(1.736e-14,1.637e-7,1.035e4)
battery_cell.create_anode(8.275e-14,3.600e-6,2.948e4)

#Reference potentials for the electrodes
#cathode_potential_ref = 
cathode_potential_ref_array = [5.502, 4.353, 3.683, 3.554, 3.493, 3.4, 
                                      3.377,3.364, 3.363, 3.326,3.324, 3.322, 
                                      3.321, 3.316, 3.313, 3.304, 3.295, 3.293,
                                      3.290,3.279 ,3.264,3.261,3.253, 3.245, 
                                      3.238, 3.225, 3.207, 2.937, 2.855, 2.852,
                                      1.026, -1.12,-1.742]

battery_cell.cathode.create_potential_lookup_tables(cathode_potential_ref_array)

#anode_potential_ref = 
anode_potential_ref_array = [3.959, 3.4, 1.874, 9.233e-1, 9.074e-1, 
                                    6.693e-1,2.481e-3,1.050e-3,1.025e-3, 8.051e-4,
                                    5.813e-4, 2.567e-4, 2.196e-4, 1.104e-4,
                                    3.133e-6,1.662e-6,9.867e-7, 3.307e-7, 1.57e-7,
                                    9.715e-8, 5.274e-9, 2.459e-9, 7.563e-11,
                                    2.165e-12,1.609e-12, 1.594e-12, 1.109e-12,
                                    4.499e-13, 2.25e-14, 1.335e-14, 1.019e-14,
                                    2.548e-16, 1.654e-16]
battery_cell.anode.create_potential_lookup_tables(anode_potential_ref_array)
        

#shorthand
cathode=battery_cell.cathode
anode=battery_cell.anode

dr_cath = R_CATHODE/N_SEGMENTS
r_cath = np.empty(len(time_history))


#Initialize the cathode
concentrations_cathode = np.zeros((N_SEGMENTS+1,len(time_history)))
#print('length time history',len(time_history))
#print('concentrations_cathode', concentrations_cathode)
concentrations_cathode[:,0] = cathode.concentration_list[28]
#print(concentrations_cathode[0,:])
#print('concentrations_cathode', concentrations_cathode)
cathode_initial_c=cathode.concentration_list[28]
#print(cathode_initial_c)
cathode.mesh_initialize(R_CATHODE, N_SEGMENTS, n_timestep, cathode_initial_c)
#print('cathode.Mesh=',cathode.Mesh.get_concentration_by_id())

anode_initial_c=anode.concentration_list[6]
anode.mesh_initialize(R_ANODE,N_SEGMENTS,n_timestep,anode_initial_c)
second_derivative(cathode.Mesh,1.0,1)

A_cathode = cathode.calculate_effective_area()
print('area cathode', A_cathode)

#for i in range(len(time_history)):
#    r_cath[i]=i*dr_cath

#for i in range(len(time_history)):
#    first_derivative(cathode.Mesh,1.0,i)
#    second_derivative(cathode.Mesh,1.0,i)


print('cathode.concentration_list:', cathode.concentration_list)
print('cathode_initial_c', cathode_initial_c)
print(len(cathode.concentration_list))
print(len(cathode_potential_ref_array))
#cathode_potential = cathode.electrode_potential(cathode.concentration_list, cathode_potential_ref_array, concentration)
#print('cathode_potential', cathode_potential)

#compute the derivatives



#generate the time history:

for i in range(n_timestep):
    cathode.simulation_step(i,DT)
    anode.simulation_step(i,DT)
    
    
voltage=battery_cell.get_voltage()