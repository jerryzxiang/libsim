'''
Node
'''
import numpy as np





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
