'''
Node

Node is a parent class for classes that describe the points in the mesh
for each type of problem. A Node is a general representation of a point 
in space. This parent class does not define the dimensionality or any 
other attributes.
'''
import numpy as np

class Node():
    '''
    Node class

    :param mesh: Mesh
    :type mesh: mesh [Mesh]
    :param node_id: Unique identifier for a node.
    :type node_id: [int]
    :param x: Index identifier for location of the node.
    :type x: x [int]

    '''
    #Right now the node class is written in a way that the coordinates do not 
    #change, they do not have time history
    def __init__(self, mesh, node_id, x):
        '''
        :param mesh: Mesh
        :type mesh: mesh [Mesh]
        :param node_id: Unique identifier for a node.
        :type node_id: [int]
        :param x: Index identifier for location of the node.
        :type x: x [int]
        '''
        self.x = np.array(x)
        self.node_id = node_id
        return
    
class Node_SPM(Node):
    '''
    Node_SPM class, subset of Node

    Inherits Node. This is the implementation of Node for SPM
    modeling.

    :param mesh: Mesh
    :type mesh: [Mesh]
    :param node_id: Unique identifier for a node.
    :type node_id: [int]
    :param x: Index Identifier for location of the node.
    :type x: [int]
    '''
    def __init__(self, mesh, node_id, x, initial_concentration):
        '''
        Initialize Node_SPM class with the
        mesh, node_id, x, initial_concentration
        '''
        #The timehistory
        self.concentration = np.zeros((1, mesh.n_timestep))
        self.concentration[0, 0] = initial_concentration
        super().__init__(mesh, node_id, x)
