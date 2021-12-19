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

def plot_concentration(electrode):
  plt.figure()
  plt.title('Concentration:' + str(electrode))
  plt.xlabel('Time [s]')
  plt.ylabel('Concentration [mol /m$^{3}$]')
  plt.plot(electrode.Mesh.node_container[10].concentration[0,:])
  plt.show()