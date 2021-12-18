import numpy as np
import math
import scipy.interpolate
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
c = np.linspace(0,Cmax_cath,33)
Cmax_an = 2.948e4;# % mol/m^3
Uref_an =[3.959, 3.4, 1.874, 9.233e-1, 9.074e-1, 
                                    6.693e-1,2.481e-3,1.050e-3,1.025e-3, 8.051e-4,
                                    5.813e-4, 2.567e-4, 2.196e-4, 1.104e-4,
                                    3.133e-6,1.662e-6,9.867e-7, 3.307e-7, 1.57e-7,
                                    9.715e-8, 5.274e-9, 2.459e-9, 7.563e-11,
                                    2.165e-12,1.609e-12, 1.594e-12, 1.109e-12,
                                    4.499e-13, 2.25e-14, 1.335e-14, 1.019e-14,
                                    2.548e-16, 1.654e-16]
a = np.linspace(0,Cmax_an,33)
t = 0.2; # simulation time. s
dt = 0.001; # change in time
timehis = np.linspace(0,t,10000)
#%% The following portion of the code will solve for the electrode potential
#% of the CATHODE
D_cath = 1.736e-14; #% Solid diffusivity of the cathode, m^2*s^-1 
R_cath = 1.637e-7; #% Particle radius in the cathode, m
N = 10; #% number of radial segments
dr_cath = R_cath/N; #% radial segment length, m
   #   % Area calculation for the CATHODE
coul_cath = 2.3*3600
mol_cath = coul_cath/F
vol_cath = mol_cath/Cmax_cath
partvol_cath = (4/3)*pi*(R_cath**3)
numpart_cath = vol_cath/partvol_cath
A_cath = numpart_cath*4*pi*(R_cath**2)
r_cath=np.zeros(N+1) # fixed indexing - this is ok

for k in range(1,N+1): # indexing is correct
    r_cath[k] = k*dr_cath 
    #print(r_cath[k])

# this indexing should be correct 
# matrix of N+1 by length of timehis
C_cath = np.zeros((N+1,len(timehis))) #% Initialize the concentration matrix

# here is where you need to pay attention to indexing
C_cath[0:N+1,0] = c[28] #% Set the initial concentration for all nodes
#print(C_cath[0:N+1,1]) # when i print, this is 11 values, same as matlab
#C_cath[N+1, len(timehis)] = 0

#% For each step in time, the following loop determines the ion conentration
#% at each node along the radius by use of the governing equation and the
#% boundary conditions
#% Note: negative input current signifies the removal of ions from the % cathode which occurs during battery charging
for j in range(0,len(timehis)):
    for i in range(2, N+1):
        rSquared = r_cath[i]**2
        print(rSquared)
        secondDer = (C_cath[i+1,j]-(2*C_cath[i,j])+C_cath[i- 1,j])/(dr_cath**2)
        #print(secondDer)
        firstDer = (C_cath[i+1,j]-C_cath[i-1,j])/dr_cath
        changeRate = ((rSquared*secondDer)+(r_cath[i]*firstDer))*D_cath/rSquared
        C_cath[i,j+1] = C_cath[i,j]+(dt*changeRate)
    C_cath[1,j+1] = C_cath[2,j+1]
    C_cath[N,j+1] = (dr_cath*(-inputCurrent)/(D_cath*A_cath*F)) + C_cath[N,j+1]

# Interpolation between the reference potential values to find the
# reference potential at a specific, calculated surface concentration
U_cath = np.zeros(len(timehis))

#for j in range(1,(len(timehis))):
#    U_cath[j] = scipy.interpolate.PchipInterpolator(c,Uref_cath,C_cath[N+1,j])

'''
# The following portion of the code will solve for the electrode potential of the ANODE
D_an = 8.275e-14 # Solid diffusivity of the anode, m^2*s^-1
R_an = 3.600e-6 # Particle radius in the anode, m
N = 10 # number of segments
dr_an = R_an/N; # segment length, m
# Area calculation for the ANODE
coul_an = 2.3*3600
mol_an = coul_an/F
vol_an = mol_an/Cmax_an
partvol_an = (4/3)*pi*(R_an**3)
numpart_an = vol_an/partvol_an
A_an = numpart_an*4*pi*(R_an**2)
r_an = np.zeros(N)
for k in range(1,N):
    r_an[k] = k*dr_an

C_an = np.zeros([N+1,len(timehis)]) # Initialize the concentration matrix
C_an[1:N+1,1] = a[7] # Set the initial concentration for all nodes
# For each step in time, the following loop determines the ion conentration
# at each node along the radius by use of the governing equation and the
# boundary conditions
# Note: positive input current signifies the addition of ions to the
# anode which occurs during battery charging
for j in range(0,(len(timehis)-1)):
    for i in range(2,N):
        rSquared = (r_an[i]**2)
        secondDer = (C_an[i+1,j]-(2*C_an[i,j])+C_an[i- 1,j])/(dr_an**2)
        print(secondDer)
        firstDer = (C_an[i+1,j]-C_an[i-1,j])/dr_an
        changeRate = ((rSquared*secondDer)+(r_an[i]*firstDer))*D_an/rSquared
    C_an[i,j+1] = C_an[i,j]+(dt*changeRate)
    C_an[1,j+1] = C_an[2,j+1]
    C_an[N,j+1] = (dr_an*(-inputCurrent)/(D_an*A_an*F)) + C_an[N,j+1]

# Interpolation between the reference potential values to find the
# reference potential at a specific, calculated surface concentration
#U_an = np.zeros(len(timehis))
#for j in range(1,(len(timehis))):
#    U_an[j] = scipy.interpolate.PchipInterpolator(c,Uref_an,C_an[N+1,j])




# Find the difference between electrode potentials and add the internal
# battery resistance term
#U_diff = U_cath - U_an
#R_internal = 0.150; # ohms
#U_internal = inputCurrent*R_internal
#batteryVoltage = U_diff + U_internal

'''


plt.figure()
plt.plot(C_cath[N,0:100])
plt.show()
