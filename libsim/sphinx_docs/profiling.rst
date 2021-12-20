Profiling and Tuning Results
============================

We ran an initial profiling assessment using cProfile on the alpha version of libsim. 
By far the slowest function in terms of runtime was simulation_step within the electrode 
class. From that analysis, it became clear that the function was a bit overloaded with 
tasks. We then refactored the stepper code into a new separate solver file to reduce 
some of this complexity. As a result, the runtime of this electrode code was reduced 
by around 90%, from 1.5 seconds to 0.15 seconds. 

At this point, the longest running portion of the code is that associated with the 
creation and plotting of the output graphs. These functions are integral to the 
usage of the library, and are executed in an efficient manner as of now utilizing pyplot. 
