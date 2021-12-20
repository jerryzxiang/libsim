'''
Derivative
'''
import numpy as np

def first_derivative(Mesh, coefficient, timestep):  
    '''
    Calculates the first derivative in Fick's Law using a "phantom node".

    :param Mesh: Mesh for which the derivative is to be evaluated.
    :type Mesh: [Mesh]
    :param coefficient: Scalar coefficient for the derivative.
    :type coefficient: [double]
    :param timestep: Index for the timestep of the current derivative.
    :type timestep: [int]
    :return: The first derivative of Fick's Law for each of the nodes in the Mesh.
    :rtype: [double]
    '''
    #The coefficient to be passed is a function
    #Mesh is the mesh for which the derivative is to be evaluated.
    
    first_derivative = np.zeros([Mesh.n_nodes, 1])
        
    #utilize a "phantom node" to be able to compute the second derivative at 
    #The edges
    for i in range(1, Mesh.n_nodes - 1):
        i_plus_1 = Mesh.get_concentration_by_id(i + 1, timestep)
        i_minus_1 = Mesh.get_concentration_by_id(i - 1, timestep)
        distance = 2.0 * (Mesh.node_container[i + 1].x - Mesh.node_container[i].x)
        first_derivative[i, 0] = (i_plus_1 - i_minus_1) / (distance)
 #       first_derivative[i, 0] = coefficient * first_derivative[i, 0]
        
    return first_derivative
        
def second_derivative(Mesh, coefficient, timestep):
    '''
   Calculates the second derivative in Fick's Law using a "phantom node".

    :param Mesh: Mesh for which the derivative is to be evaluated.
    :type Mesh: [Mesh]
    :param coefficient: Scalar coefficient for the derivative.
    :type coefficient: [double]
    :param timestep: Index for the timestep of the current derivative.
    :type timestep: [int]
    :return: The second derivative of Fick's Law for each of the nodes in the Mesh.
    :rtype: [double]
    '''
    second_derivative = np.zeros([Mesh.n_nodes, 1])
    
    #utilize a "phantom node" to be able to compute the second derivative at 
    #The edges
    for i in range(1, Mesh.n_nodes - 1):
        i_plus_1 = Mesh.get_concentration_by_id(i + 1, timestep)
        i_minus_1 = Mesh.get_concentration_by_id(i - 1, timestep)
        i_center = Mesh.get_concentration_by_id(i, timestep)
        distance = Mesh.node_container[i + 1].x - Mesh.node_container[i].x
        try:
            second_derivative[i, 0] = (i_plus_1 - 2 * i_center + i_minus_1) / (distance ** 2)
        except:
            print("error on timestep")
            print(timestep)
            raise
        second_derivative[i, 0] = coefficient * second_derivative[i, 0]    
    return second_derivative