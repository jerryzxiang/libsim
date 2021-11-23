#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 09:50:12 2021

@author: antti
"""


from abc import ABC, abstractmethod

class TemporalIntegrator(ABC):
    
    
    def __init__(self):
        pass
    
    
    @abstractmethod
    def step(self):
        pass