#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 09:28:22 2021

@author: antti
"""

from abc import ABC, abstractmethod
 
class SpatialSolver(ABC):
 
    
    def __init__(self, mesh,RHS):
        pass
    
    @abstractmethod
    def update_mesh(self):
        pass
    
    
    
    
    
 
