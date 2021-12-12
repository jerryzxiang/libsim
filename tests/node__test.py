#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 20:53:05 2021

@author: antti

"""
from libsim.node import Node_SPM as Node_SPM


class MockMesh:
   def __init__(self,n_timestep):
        self.n_timestep=n_timestep

def test_spm_initial_concentration():
    mesh=MockMesh(10)
    node=Node_SPM(mesh,1,10,20)
    assert node.concentration[0,0]==20
    
def test_spm_x():
    mesh=MockMesh(10)
    node=Node_SPM(mesh,1,10.0,20)
    assert node.x==10
    
def test_spm_node_id():
    mesh=MockMesh(10)
    node=Node_SPM(mesh,1,10.0,20)
    assert node.node_id==1