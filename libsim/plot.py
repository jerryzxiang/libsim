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
def plot_voltage(time, voltage):
  plt.figure()
  plt.title('Voltage')
  plt.xlabel('Time [s]')
  plt.ylabel('Potential [V]')
  plt.plot(time, voltage)
  plt.show()

def plot_concentration(time, electrode, electrode_type):
  plt.figure()
  plt.title(electrode_type +' ion concentration')
  plt.xlabel('Time [s]')
  plt.ylabel('Ion concentration [mol /m$^{3}$]')
  plt.plot(time, electrode.Mesh.node_container[10].concentration[0,:])
  plt.show()