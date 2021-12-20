'''
Mesh 

Parent class for classes that describe the computational mesh for each
different type of model/problem.
'''
from node import Node_SPM as Node_SPM
from node import Node as Node

class Mesh1D():
    '''
    Mesh 1D is a 1-dimensional mesh composed of Nodes complete with
    functions to create Nodes. It includes an indexing system in order
    to be able to access individual nodes as needed (post-processing).

    In order to initialize a Mesh1D, a variable n_timestep is needed.

    :param n_timestep: Number of timesteps to be taken.
    :type n_timestep: [int]
    '''
    #Need to make init empty, while creating mesh it is not really necessary
    #To know the lengths etc. This is better done in some separate generator
    #This way there is flexibility in how the mesh is created.
    def __init__(self, n_timestep):
        '''
        Initialize Mesh1D class with
        
        :param n_timestep: Number of timesteps to be taken.
        :type n_timestep: [int]
        '''
        self.node_id = 0
        #Initialize the container (list in this implementation holding the nodes)
        self.node_container = []
        self.n_timestep = n_timestep
        self.n_nodes = 0

    def add_node(self, x):
        '''
        Adds a node based on x location, and returns a new node.

        :param x: Index identifier for location of the node.
        :type x: [int]
        :return: x
        :rtype: [int]

        '''
        self.node_container.append(Node(self, self.node_id, x))
        self.node_id += 1
        self.n_nodes += 1

        return

    def add_nodes(self, length, n_elements):
        '''
        Add nodes of a specified length with n_elements.

        :param length: Length of nodes to add.
        :type length: [int]
        :param n_elements: Number of nodes to add.
        :type n_elements: [int]
        '''
        #helper variables
        self.dr = length / n_elements
        x = 0.0
        for i in range(n_elements + 1):
            self.add_node(x + i * self.dr)
            
class Mesh1D_SPM(Mesh1D):
    '''
    Mesh1D_SPM class inherits Mesh1D. Here the one dimensional Mesh
    is implemented for the use with SPM model.
    '''
    def add_node(self, x, initial_concentration):
        '''
        Adds a node based on x location.

        :param x: Index identifier for location of the node.
        :type x: [int]
        :param initial_concentration: Initial concentration of ions at each node. [mol/(m^3)]
        :type initial_concentration: [double]
        '''
        self.node_container.append(Node_SPM(self, self.node_id, x, initial_concentration))
        assert len(self.node_container) == self.node_id + 1
        self.node_id += 1
        self.n_nodes += 1
        return
    
    def add_nodes(self, length, n_elements, initial_concentration):
        '''
        Add nodes of a length with n_elements

        :param length: Length of nodes to add.
        :type length: [int]
        :param n_elements: Number of nodes to add.
        :type n_elements: [int]
        :param initial_concentration: Initial concentration of ions at each node. [mol/(m^3)]
        :type initial_concentration: [double]
        '''
        #helper variables
        self.dr = length / n_elements
        x = 0.0
        for i in range(n_elements + 1):
            self.add_node(x + i * self.dr, initial_concentration)
                
    def get_concentration_by_id(self, node_id, timestep):
        '''
        Get concentration at a node, and return

        Add nodes of a specified length with n_elements.

        :param node_id: Unique identifier for a node.
        :type node_id: [int]
        :param timestep: Current timestep.
        :type timestep: [int]
        :return: Node concentration
        :rtype: [double]
        '''
        return self.node_container[node_id].concentration[0, timestep]