"""
Information for battery anode and cathode parameters.
There are 3 types of cathodes: LFP, LCO, and NMC.
Each cathode has parameters for diffusivity,
particle radius, and maximum ion concentration. 
Similarly, there are 2 types of anodes: 
diffusivity,particle_radius,max_ion_concentration
"""
cathodeDict = {
    "LFP": [5.900E-18, 1.000E-8, 2.281E4],
    "LCO": [1.736E-14, 1.637E-7, 1.035E4],
    "NMC": [1.000E-14, 5.300E-6, 4.823E4],
    "NCA": [3.000E-15, 1.633E-6, 4.900E4],
    }

anodeDict = {
    "graphite": [3.300E-14, 5.860E-6, 3.313E4],
}
