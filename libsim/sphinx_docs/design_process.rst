Design Process
==============

In this code suite, abstracting battery behavior was not a trivial task. 
LIBs can be designed with many different types of anodes and cathodes 
which directly affect the electro-chemical properties and electrolyte 
interactions. To capture this variability, we decided to create a 
dictionary of different lithium-ion battery types that each have 
their own unique properties regarding diffusivity, particle radius, 
and ion concentration. This increases the versatility of the code 
suite to make the simulations widely applicable should an end user 
decide to test through various types of lithium-ion batteries of 
their choosing. 

SPM model was used to simulate battery cycling behaviors. For 
generating solutions a finite element method was chosen. 
Architectural choices were made to allow for future 
implementation of various different model types.

UML DIAGRAM
-----------
INCLUDE NEW UML DIAGRAM