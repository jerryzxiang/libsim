#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 16:22:27 2021

@author: antti
"""
from libsim.derivative import first_derivative as first_derivative
from libsim.derivative import second_derivative as second_derivative

FARADAY_NUMBER = 9.64853399e4


def simulation_step(electrode, timestep_id, dt):
    '''
    Advances the simulation one step
    '''
    #Take the euler step for the interior nodes
    euler_step(electrode,timestep_id,dt)
    # Apply the Neumann condition at the center of particel (zero derivative)
    apply_neumann_bc(electrode.Mesh, timestep_id)
    # Calculate surface concentration
    surface_c =calculate_surface_concentration(electrode, timestep_id)
    # Apply the dirichlet BC, set the final node concentration to the surface 
    #concentration
    apply_dirichlet_bc(electrode.Mesh, timestep_id, surface_c)
    # Fill out potential_history array at each timestep with interpolated value
    # self.potential_history[timestep_id] = self.potential_interpolator(self.concentration_list, self.reference_potential)
    electrode.potential_history[timestep_id]=electrode.potential_interpolator(surface_c)




def euler_step(electrode,timestep_id,dt):
    
    arg1 = first_derivative(electrode.Mesh, 1.0, timestep_id)
    arg2 = second_derivative(electrode.Mesh, 1.0, timestep_id)
    n_nodes = len(arg1)
    for i in range(1, electrode.Mesh.n_nodes - 1):
        node = electrode.Mesh.node_container[i]
        r = node.x

        r_squared = r ** 2
        coef1 = r_squared
        coef2 = r * electrode.diffusivity / r_squared
        # Update concentration of current node container with
        # previous concentration plus dt * value
        electrode.Mesh.node_container[i].concentration[0, timestep_id] = (
            electrode.Mesh.node_container[i].concentration[0, timestep_id - 1] +
            dt * (coef1 * arg1[i] + coef2 * arg2[i]))
        
        
        
def apply_neumann_bc(mesh,timestep_id):
    mesh.node_container[0].concentration[0, timestep_id] = (
        mesh.node_container[1].concentration[0, timestep_id])
    return 0



def apply_dirichlet_bc(mesh,timestep_id,surface_c):
    n_nodes=mesh.n_nodes
    # Set concentration at final node container to be surface concentration
    mesh.node_container[n_nodes-1].concentration[0, timestep_id] = (surface_c +
                         mesh.node_container[n_nodes- 2].concentration[0, timestep_id])
    
def calculate_surface_concentration(electrode,timestep_id):
    n_nodes=electrode.Mesh.n_nodes
    surface_c = ((electrode.Mesh.dr * (electrode.input_current) /
                 electrode.effective_area * electrode.diffusivity * FARADAY_NUMBER) +
                 electrode.Mesh.node_container[n_nodes - 2].concentration[0, timestep_id])
    return surface_c