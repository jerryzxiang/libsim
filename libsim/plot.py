# module to plot battery parameters over time
import numpy as np
import argparse
import matplotlib.pyplot as plt

from batterycell import BatteryCell as BatteryCell
from mesh import Mesh1D_SPM as Mesh1D_SPM
import parameters.paramLibrary as pl
import parameters.referencePotentials as rp
