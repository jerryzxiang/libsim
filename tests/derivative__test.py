#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 13:08:14 2021

@author: antti
"""
import pytest
import numpy as np
from libsim.mesh import Mesh1D_SPM as Mesh1D_SPM
from libsim.derivative import first_derivative as first_derivative
from libsim.derivative import second_derivative as second_derivative


length=10.0
n_elements=10
dr=1.0
initial_concentration=7.0
x_0=0.0
n_timestep=10
mesh=Mesh1D_SPM(n_timestep)
mesh.add_nodes(length,n_elements,initial_concentration)

timestep=0

#create the parameter list
#no need to go through all of the indices, since first and last in the derivative
#are not computed.
test_parameter_list=[]
for i in range(1,10):
    test_parameter_list.append((i,0.0))
    

@pytest.mark.parametrize('inp, expected', test_parameter_list)
def test_first_derivative_initial(inp,expected):
    d1=first_derivative(mesh,1.0,timestep)
    comparison=np.zeros([mesh.n_nodes-2])
    assert d1[inp,0]==expected
    
mesh.node_container[2].concentration[0,0]=2




def test_first_derivative_1():
    d1=first_derivative(mesh,1.0,timestep)
    comparison=np.zeros([mesh.n_nodes-2])
    assert d1[1,0]==1.0