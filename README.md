# abm_framework

<img src="https://github.com/LinnartSF/logos/blob/main/main1.png" alt="SCDA - Supply Chain Data Analytics" title="">

A framework for agent-based simulation. It covers grid-based simulations. This model is part of SCDA.

The model supports grid-based simulations and includes visualization and animation functionality. The module is continously extended to cover additional functionality. For example, I added the Moore neighbourhood as a neighbourhood option for grid-based ABM simulations. In a second step, the Neumann neighbourhood (easy addition) can be added, and then in addition other neighbourhood types as required.

<h2>abm framework module content</h2>

Database directory contains <strong>sqlite3</strong> database file that is meant for storing simulation results into database.

The <strong>data.py</strong> module provides functionality for executing queries in the database. <strong>data.py</strong> comprises a <strong>Database class</strong> and a <strong>Manager class</strong>. <strong>Database class</strong> facilitates connection to <strong>sqlite3</strong> and potentially also <strong>mssql database</strong>. <strong>Manager class</strong> provides methods representing standardized queries for quickly implementing operations on the database that are of relevance to the ABM simulations supported by this package.

<strong>framework.py</strong> contains classes for modelling e.g. the simulation environment and the agents themselves.

<strong>stats.py</strong> provides visualization capabilities for visualizing simulation results.

<strong>config.py</strong> is a configuration file that e.g. allows for path adjustments or input parameter adjustments. It e.g. specifies the filepath of the <strong>sqlite3</strong> database used to store simulation results.

<strong>animation.py</strong> provides animation capabilities for animating simulation results and their trajectory throughout time.

<h2>references to related articles covering abm modeling</h2>

I gave some basic introductions covering the differences between simulation methods as well as basic agent-based simulation modeling in Python -  and you can find these introductions on my blog:
- <a href="https://www.supplychaindataanalytics.com/simulation-methods-for-scm-analysts/">Simulation methods for SCM analysts</a>
- <a href="https://www.supplychaindataanalytics.com/developing-a-simple-agent-based-simulation-model-in-python/">Developing a simple agent-based simulation model in Python</a>
- <a href="https://www.supplychaindataanalytics.com/a-simple-agent-based-simulation-run-visualized-using-matplotlib-in-python/">A simple agent-based simulation run visualized with matplotlib in Python</a>
- <a href="https://www.supplychaindataanalytics.com/agent-based-modeling-in-python/">Agent-based modeling in Python</a>

<h2>introduction to agent-based simulation</h2>

Agent-based simulation is a methodology that applies compulation models for simulating interactions between autonomous agents as well as their actions. It can be combined with other simulation methodes, e.g. with monte-carlo simulation methodology for consideration of stochasticity. But it can e.g. also be combined with discrete-event simulation methodology. For example, processes "going on" inside agents can be modelled and simulated with discrete-event simulation. Below is an overview and comparison of the main simulation methodes.

<img src="/docufigs/simulationmethods.PNG" alt="Simulation method comparison" title="">

Agent-based simulation models are simulation models that focus that describe microscopic interactions between agents. By adding, removing, and manipulating these microscopic interactions, changes to macroscopic system behaviour are analyzed. ABM is applied to understand the emergence of complex macropic phenomena.

<img src="/docufigs/abm.PNG" alt="Agent attributes and interactions" title="">

Agents have attributes and the interactions between agents are described by logics and strategies. This framework provides a toolkit for building agent-based models. It also provides pre-defined database structures and visualization as well as animation functionality. You can use this to implment your own agent-based simulation. Demo models are provided in the demos folder.

<h2>agent-based modeling applications</h2>

Agent-based simulation models are applied in many different areas. This includes the domains listed below:
1) Biology
2) Epidemology 
3) Business
4) Technology
5) Network technology
6) Social sciences
7) Economics
8) Autonomous driving

This repository comprises a demos folder. In there you will find, dynamically added over time, a series of simulation examples. 

<h2>exemplary visualizations created with abm_framework</h2>

This framework supports standardized agent-based simulation animations and visualizations. The scope of animation and visualization templates is dynamically expanded overtime, but initially comprises at least:
- agent attribute value trajectories for all agents individually, a specific subset of agents, or all agents on average
- average attribute value distribution over time, for a specific population of agents and a list of relevant agent attributes
- grid location plots and animations for all agents or a set of agent population groups
- attribute value density distribution across the grid, in the form of plots and animations, for specified attributes

You can see some exmaples below: 

<img src="/docufigs/segregationprocess.gif" alt="Segregation process animation" title="">

<img src="/docufigs/segregationutility.gif" alt="Segregation process and utility concentration" title="">

<img src="/docufigs/avglifeplot.png" alt="Avg agent attribute value trajectory" title="">

<img src="/docufigs/lifeplot.png" alt="Agent attribute value trajectories" title="">

<img src="/docufigs/human_locations.png" alt="Agent grid locations" title="">

<img src="/docufigs/infectionanimation2.gif" alt="Attribute density animation" title="">

<img src="/docufigs/recoveryanimation2.gif" alt="Attribute density animation" title="">

<img src="/docufigs/avgstates.png" alt="Attribute density animation" title="">  
