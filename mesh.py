#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 16:59:37 2021

@author: antti
"""


from node import Node_SPM as Node_SPM
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
        