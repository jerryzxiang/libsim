#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 21:13:37 2021

@author: antti
"""

import pytest

from libsim.mesh import Mesh1D_SPM as Mesh1D_SPM


n_timestep=10
length=10.0
n_elements=10
dr=1.0
initial_concentration=7.0
x_0=0.0
mesh=Mesh1D_SPM(n_timestep)
    

test_parameter_list=[]
for i in range(1,10):
    test_parameter_list.append((i,initial_concentration))
    

@pytest.mark.parametrize('inp, expected', test_parameter_list)
def test_spm_add_single_node(inp,expected):
    

    mesh.add_node(x_0,initial_concentration)
    node=mesh.node_container[inp]
    assert node.concentration[0,0]==initial_concentration


def test_spm_add_nodes():
    
    n_timestep=10
    length=10.0
    n_elements=10
    dr=1.0
    initial_concentration=7.0
    x_0=0.0
    mesh=Mesh1D_SPM(n_timestep)
    mesh.add_nodes(length,n_elements,initial_concentration)
    
    node=mesh.node_container[0]
    assert mesh.n_nodes==11
    assert mesh.node_id==11
    assert len(mesh.node_container)==11
    
    assert node.node_id==0
    assert node.x==x_0
    assert node.concentration[0,0]==initial_concentration
    
    node5=mesh.node_container[4]
    assert node5.node_id==4
    assert node5.x==4.0
    assert node5.concentration[0,0]==initial_concentration
    
def test_get_concentration_by_id():
    n_timestep=10
    length=10.0
    n_elements=10
    dr=1.0
    initial_concentration=7.0
    x_0=0.0
    mesh=Mesh1D_SPM(n_timestep)
    mesh.add_nodes(length,n_elements,initial_concentration)
    
    node=mesh.node_container[0]
    assert mesh.get_concentration_by_id(0,0)==initial_concentration
    
    node5=mesh.node_container[4]
    assert node5.node_id==4
    assert node5.x==4.0
    assert mesh.get_concentration_by_id(4,0)==initial_concentration
    

    

n_timestep=10
length=10.0
n_elements=10
dr=1.0
initial_concentration=7.0
x_0=0.0
mesh=Mesh1D_SPM(n_timestep)
mesh.add_nodes(length,n_elements,initial_concentration)
    

test_parameter_list=[]
for i in range(1,10):
    test_parameter_list.append((i,initial_concentration))
    

@pytest.mark.parametrize('inp, expected', test_parameter_list)
def test_concentration(inp,expected):
    assert mesh.node_container[inp].concentration[0,0]==initial_concentration
    assert mesh.get_concentration_by_id(inp,0)==initial_concentration
    

    
    
#test_parameter_list=[]
#for i in range(n_timestep):
#    test_parameter_list.append((i,2.0))
    

#@pytest.mark.parametrize('inp, expected', test_parameter_list) 
mesh.node_container[2].concentration[0,0]=2 
def test_concentration_set():
    n_timestep=10
    length=10.0
    n_elements=10
    dr=1.0
    initial_concentration=7.0
    x_0=0.0
    mesh=Mesh1D_SPM(n_timestep)
    mesh.add_nodes(length,n_elements,initial_concentration)
    mesh.node_container[2].concentration[0,0]=2.0
    assert mesh.node_container[2].concentration[0,0]==2.0