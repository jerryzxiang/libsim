Background
==========

Models
------

One of the research challenges in the development of lithium-ion batteries 
(LIBs) is to predict their behavior under different operating modes, 
useful for estimating state of charge and state of health of batteries 
in electric vehicles (EV’s). There exist empirical models, mostly equivalent 
circuit-based, widely used in the Battery Management Systems (BMS) of 
electronics and EV’s. These types of models use past experimental data of a 
battery to anticipate its future states. Most of the experimental data used 
to find charge/discharge characteristics rely on the current or cell 
potential. On one hand, these empirical models are relatively fast and 
simple computationally, but they have drawbacks. For example, the 
physics-based parameters are not able to be predetermined. The battery 
characteristics aren’t updated as the battery ages and a battery’s model 
is unique to itself - it does not apply to all batteries but only a specific 
type. 

Other major types of models are Pseudo-two-Dimensional (P2D) and Single 
Particle Model (SPM). Both popular battery models are widely used today. 
The P2D model is commonly used in lithium-ion battery studies, and the 
predicted behavior of this model matches experimental data quite accurately. 
A significant drawback with this model is the difficulty to use in real-time 
due to its computationally expensive nature. The SPM model simplifies 
anode/cathode interactions and reduces the dimensionality down to one 
dimension, which greatly enhances its computational capabilities. However, 
it places greater importance on the parameters of the anodes and cathodes. 


