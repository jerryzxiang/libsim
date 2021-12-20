Usage
=====


.. _installation:

Installation
------------
The third-party packages required are: `python3`, `numpy`, `scipy.interpolate`, 
`math`, and `matplotlib`. These packages can all be installed via `pip3`.

The repo can be cloned from `https://github.com/jerryzxiang/libsim.git` or 
installed via 

.. code-block:: console
   pip3 install git+ssh://git@github.com:jerryzxiang/libsim.git

Modeling Batteries
------------------

This program is run through the driver code file, `main.py`, which takes 8 
command line arguments. As of now, there is no GUI. The inputs are the cathode, 
anode, input current, capacity of the cell in amp hours, the number of radial 
segments, the simulation time in seconds, and the time steps. An example is 
shown here for an LIB with an LFP cathode and graphite anode:

.. code-block:: console
   python3 main.py 'LFP' 'graphite' 0.5 2.3 1.5 10 10 0.001

To get help, use `python3 main.py -h'`.



.. code-block:: console

   $ git clone https://github.com/jerryzxiang/libsim.git

