#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import math
pi=math.pi
inputCurrent=0.5
import matplotlib.pyplot as plt
#singleParticle.m
# This code simulates a single particle battery model % Last edit: AEH 2_24_15

# The input current is chosen as the input to the model inputCurrent = 0.5; % Amperes
F = 9.64853399e4; #% C/mol
# Reference potentials for each electrode at a concentration value ranging
# from no ions to a maximum value
Cmax_cath = 1.035e4; #% mol/m^3
Uref_cath =  [5.502, 4.353, 3.683, 3.554, 3.493, 3.4, 
                                      3.377,3.364, 3.363, 3.326,3.324, 3.322, 
                                      3.321, 3.316, 3.313, 3.304, 3.295, 3.293,
                                      3.290,3.279 ,3.264,3.261,3.253, 3.245, 
                                      3.238, 3.225, 3.207, 2.937, 2.855, 2.852,
                                      1.026, -1.12,-1.742]
c = np.linspace(0,Cmax_cath,33);
Cmax_an = 2.948e4;# % mol/m^3
Uref_an =[3.959, 3.4, 1.874, 9.233e-1, 9.074e-1, 
                                    6.693e-1,2.481e-3,1.050e-3,1.025e-3, 8.051e-4,
                                    5.813e-4, 2.567e-4, 2.196e-4, 1.104e-4,
                                    3.133e-6,1.662e-6,9.867e-7, 3.307e-7, 1.57e-7,
                                    9.715e-8, 5.274e-9, 2.459e-9, 7.563e-11,
                                    2.165e-12,1.609e-12, 1.594e-12, 1.109e-12,
                                    4.499e-13, 2.25e-14, 1.335e-14, 1.019e-14,
                                    2.548e-16, 1.654e-16]
a = np.linspace(0,Cmax_an,33);
t = 0.2; #% simulation time. s
dt = 0.001; #% change in time
timehis = np.linspace(0,t,10000)
#%% The following portion of the code will solve for the electrode potential
#% of the CATHODE
D_cath = 1.736e-14; #% Solid diffusivity of the cathode, m^2*s^-1 
R_cath = 1.637e-7; #% Particle radius in the cathode, m
N = 10; #% number of radial segments
dr_cath = R_cath/N; #% radial segment length, m
   #   % Area calculation for the CATHODE
coul_cath = 2.3*3600;
mol_cath = coul_cath/F;
vol_cath = mol_cath/Cmax_cath; partvol_cath = (4/3)*pi*(R_cath**3); numpart_cath = vol_cath/partvol_cath; A_cath = numpart_cath*4*pi*(R_cath**2);
r_cath=[]
for k in range(1,N+2):
    r_cath.append( k*dr_cath)

C_cath = np.zeros([N+1,len(timehis)]) #% Initialize the concentration matrix
C_cath[0:N+1,1] = c[29] #% Set the initial concentration for all nodes
#% For each step in time, the following loop determines the ion conentration
#% at each node along the radius by use of the governing equation and the
#% boundary conditions
#% Note: negative input current signifies the removal of ions from the % cathode which occurs during battery charging
for j in range(0,(len(timehis)-1)):
    for i in range(2,N):
        rSquared = (r_cath[i]**2);
        secondDer = (C_cath[i+1,j]-(2*C_cath[i,j])+C_cath[i- 1,j])/(dr_cath**2);
        firstDer = (C_cath[i+1,j]-C_cath[i-1,j])/dr_cath;
        changeRate = ((rSquared*secondDer)+(r_cath[i]*firstDer))*D_cath/rSquared;
    C_cath[i,j+1] = C_cath[i,j]+(dt*changeRate)
    C_cath[1,j+1] = C_cath[2,j+1];
    C_cath[N,j+1] = (dr_cath*(-inputCurrent)/(D_cath*A_cath*F)) + C_cath[N,j+1];


plt.plot(C_cath[N,0:100])