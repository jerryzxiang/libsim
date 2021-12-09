"""
Information for battery anode and cathode parameters.

There are 3 types of cathodes: LFP, LCO, and NMC.
Each cathode has parameters for diffusivity,
particle radius, and maximum ion concentration. 

Similarly, there are 2 types of anodes: 

diffusivity,particle_radius,max_ion_concentration
"""
import pprint

def cathodeDict():
    cathdict = {
    "LFP": [5.900E-18, 1.000E-8, 2.281E4],
    "LCO": [1.736E-14, 1.637E-7, 1.035E4],
    "NMC": [1.000E-14, 5.300E-6, 4.823E4],
    # "NCA": [],
    }
    return cathdict

class immutableCathDict:
    def __init__(self):
        self.params = cathodeDict()
        pass
    def getParams(self):
        return self.params.copy()

def anodeDict():
    anodedict = {
    "GRAPHITE": [3.300E-14, 5.860E-6, 3.313E4],
    }
    return anodedict

class immutableAnodeDict:
    def __init__(self):
        self.params = anodeDict()
        pass
    def getParams(self):
        return self.params.copy()

if __name__ == "__main__":
    cathodeDict()