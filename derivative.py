#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 14:56:26 2021

@author: antti
"""

from abc import ABC, abstractmethod


class Derivative(ABC):
    
    @abstractmethod
    def derivative_value(self,x):
        pass
     




