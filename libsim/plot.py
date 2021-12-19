# module to plot battery parameters over time
import matplotlib.pyplot as plt

from batterycell import BatteryCell as BatteryCell
from mesh import Mesh1D_SPM as Mesh1D_SPM

# plotting voltage vs time
def plot_voltage(voltage):
  plt.figure()
  plt.plot(voltage[0:9999])

def plot_concentration(cathode):
  plt.figure()
  plt.plot(cathode.Mesh.node_container[10].concentration[0,:])

def show_plots():
  plt.show()
