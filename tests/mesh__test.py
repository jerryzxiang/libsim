#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 21:13:37 2021

@author: antti
"""


from libsim.mesh import Mesh1D_SPM as Mesh1D_SPM



def test_spm_add_single_node():
    
    n_timestep=10
    length=10.0
    n_elements=10
    dr=1.0
    initial_concentration=7.0
    x_0=5.0
    mesh=Mesh1D_SPM(n_timestep)
    mesh.add_node(x_0,initial_concentration)
    
    node=mesh.node_container[0]
    assert mesh.n_nodes==1
    assert mesh.node_id==1
    assert len(mesh.node_container)==1
    assert node.node_id==0
    assert node.x==x_0
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