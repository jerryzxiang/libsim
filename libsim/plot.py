'''
module to plot battery parameters over time
'''
import numpy as np
import matplotlib.pyplot as plt

from batterycell import BatteryCell as BatteryCell
from mesh import Mesh1D_SPM as Mesh1D_SPM
import parameters.paramLibrary as pl
import parameters.referencePotentials as rp

# plotting voltage vs time
def plot_voltage(voltage, title):
  plt.figure()
  plt.title(title)
  plt.xlabel('Time [min]')
  plt.ylabel('Potential [V]')
  plt.plot(voltage)
  plt.show()

# plotting ion concentration vs time
def plot_concentration(time, electrode, electrode_type):
  plt.figure()
  plt.title(electrode_type + 
            ' Equilibrium Potential vs Ion Concentration')
  plt.xlabel('Ion concentration [mol /m$^{3}$]')
  plt.ylabel('Equilibrium Potential [V]')
  plt.plot(time, electrode.Mesh.node_container[10].concentration[0,:])
  plt.show()