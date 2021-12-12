import sys
  
# setting path
sys.path.append('..')

import main
import csv
#from math import isclose

data = []
with open('cath_conlist_default.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row)

def test_cathode_output():
    cath = main.cathode.concentration_list
    cath_m = data[0]
    for i in range(33):
        #assert isclose(cath[i], float(cath_m[i]), abs_tol = 1e-4)
        assert(cath[i] == float(cath_m[i+1]))

def test_anode_output():
    anode = main.anode.concentration_list
    
    anode_m = data[1]
    for i in range(32):
        #assert isclose(anode[i], float(anode_m[i]), abs_tol = 1e-4)
        assert(anode[i] == float(anode_m[i+1]))
