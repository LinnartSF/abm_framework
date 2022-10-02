# abm_framework
A framework for agent-based simulation. It covers grid-based simulations. 

The model supports grid-based simulations and includes visualization and animation functionality. The module is continously extended to cover additional functionality. For example, I added the Moore neighbourhood as a neighbourhood option for grid-based ABM simulations. In a second step, the Neumann neighbourhood (easy addition) can be added, and then in addition other neighbourhood types as required.

Database directory contains sqlite3 database file that is meant for storing simulation results into database.
The data.py module provides functionality for executing queries in the database.
framework.py contains classes for modelling e.g. the simulation environment and the agents themselves.
stats.py provides visualization capabilities for visualizing simulation results.
config.py is a configuration file that e.g. allows for path adjustments or input parameter adjustments.
animation provides animation capabilities for animating simulation results and their trajectory throughout time.


I gave some basic introductions covering the differences between simulation methods as well as basic agent-based simulation modeling in Python -  and you can find these introductions on my blog:


<a href="https://www.supplychaindataanalytics.com/simulation-methods-for-scm-analysts/">Simulation methods for SCM analysts</a>


<a href="https://www.supplychaindataanalytics.com/developing-a-simple-agent-based-simulation-model-in-python/">Developing a simple agent-based simulation model in Python</a>


<a href="https://www.supplychaindataanalytics.com/a-simple-agent-based-simulation-run-visualized-using-matplotlib-in-python/">A simple agent-based simulation run visualized with matplotlib in Python</a>


<a href="https://www.supplychaindataanalytics.com/agent-based-modeling-in-python/">Agent-based modeling in Python</a>
