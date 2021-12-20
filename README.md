# libsim
Final project for APC524 Fall 2021, Princeton University. Single-particle modelling for lithium-ion batteries (LIBs).

## Authors
By [Alex Caldwell](https://github.com/awcald), [Alex Preston](https://github.com/alexandercpreston), [Antti Valkonen](https://github.com/valkonena), [Jerry Xiang](https://github.com/jerryzxiang/), [Jose Yanez](https://github.com/masterjose3000).

## Installation
The third-party packages required are: 'python3', 'numpy', 'scipy.interpolate', 'math', and 'matplotlib'. 

The repo can be cloned from 'https://github.com/jerryzxiang/libsim.git'

## Usage
This program is run through the driver code file, 'main.py', which takes 8 command line arguments. As of now, there is no GUI. The inputs are the cathode, anode, input current, capacity of the cell in amp hours, the number of radial segments, the simulation time in seconds, and the time steps. An example is shown here:

'python3 main.py 'LFP' 'graphite' 0.5 2.3 1.5 10 10 0.001'

To get help, use 'python3 main.py -h'.

## Background
One of the research challenges in the development of lithium-ion batteries (LIBs) is to predict their behavior under different operating modes, which is useful for estimating state of charge and state of health of batteries in electric vehicles (EVs). There exist empirical models, mostly equivalent circuit-based, widely used in the Battery Management Systems (BMS) of electronics and EVs. These types of models use past experimental data of a battery to anticipate its future states. Most of the experimental data used to find charge/discharge characteristics rely on the current or cell potential. On one hand, these empirical models are relatively fast and simple computationally, but they have drawbacks. For example, the physics-based parameters are not able to be predetermined. The battery characteristics are not updated as the battery ages and a battery’s model is unique to itself - it does not apply to all batteries but only a specific type.

Electrochemical models are, on the other hand, more sophisticated. These models are based on chemical/electrochemical kinetics and transport equations. They may be used to simulate the LIB's characteristics and reactions. Popular electrochemical models are the Pseudo-two-Dimensional (P2D) Model and Single Particle Model (SPM). The P2D model is commonly used in lithium-ion battery studies, and the predicted behavior of this model matches experimental data quite accurately. A significant drawback with this model is the difficulty to use in real-time due to its computationally expensive nature. The SPM model simplifies anode/cathode interactions and reduces the dimensionality down to one dimension, which greatly enhances its computational capabilities. However, it places greater importance on the parameters of the anodes and cathodes.


[1] Hake, Alison. SINGLE-PARTICLE MODELING AND EXPERIMENTAL PARAMETER IDENTIFICATION FOR A LITHIUM-COBALT-OXIDE BATTERY CELL. https://honors.libraries.psu.edu/files/final_submissions/3057