Background
==========

Models
------

One of the research challenges in the development of lithium-ion batteries 
(LIBs) is to predict their behavior under different operating modes, which 
is useful for estimating state of charge and state of health of batteries 
in electric vehicles (EVs). There exist empirical models, mostly equivalent 
circuit-based, widely used in the Battery Management Systems (BMS) of 
electronics and EVs. These types of models use past experimental data of a 
battery to anticipate its future states. Most of the experimental data used 
to find charge/discharge characteristics rely on the current or cell potential. 
On one hand, these empirical models are relatively fast and simple computationally, 
but they have drawbacks. For example, the physics-based parameters are not 
able to be predetermined. The battery characteristics are not updated as the 
battery ages and a battery’s model is unique to itself - it does not apply to 
all batteries but only a specific type.

Electrochemical models are, on the other hand, more sophisticated. These 
models are based on chemical/electrochemical kinetics and transport equations. 
They may be used to simulate the LIB's characteristics and reactions. Popular 
electrochemical models are the Pseudo-two-Dimensional (P2D) Model and Single 
Particle Model (SPM). The P2D model is commonly used in lithium-ion battery 
studies, and the predicted behavior of this model matches experimental data q
uite accurately. A significant drawback with this model is the difficulty to 
use in real-time due to its computationally expensive nature. The SPM model 
simplifies anode/cathode interactions and reduces the dimensionality down to 
one dimension, which greatly enhances its computational capabilities. However, 
it places greater importance on the parameters of the anodes and cathodes.


