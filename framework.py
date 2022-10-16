"""

Module that provides a framework in the form of a class library that aids agent-based simulation modeling

The module only covers grid-based simulations

Classes comprise
- environment
- agent

Module requires random module

"""

# TODO catch and handle infeasible user input
# TODO add additional typewriting to class atrributes
# TODO support other query languages than SQLite (where differences apply)

__author__ = "Linnart Felkl"
__email__ = "linnartsf@gmail.com"

# required modules
import random
import data    # from package

def warning(msg: str) -> None:
    """ internal but also externally accessible function for printing warning message (used for faulty user input) """
    print(f"WARNING: {msg}")

# TODO: environment that agent is added to should be a attribute of the agent, but not in the attribute dictionary; set by environment when adding agent
# TODO: environment should be able to add agent, but agent should also be able to add itself to anvironment
# TODO: environment should be optional argument when creating agent instance (constructor call)
# TODO: agent class too should support obtaining the neighbourhood, by calling the environments' relevant methods
# agent class
class Agent:
    """ Agents have attributes that can be relevant to a simulation """
    def __init__(self,
                 id: int,
                 pop: str):
        self.ID = id
        self.Population = pop
        self.Row = 0 # default value, "unassigned"
        self.Col = 0 # default value, "unassigned"

        # placeholder for attribute dictionary
        self.Attributes = {}
    
    def add_attribute(self,
                      attr: str,
                      val: any) -> None:
        """ method adds attr to attributes dictionary, with the specified initial value """
        self.Attributes[attr] = val
    
    def set_attr_value(self,
                       attr: str,
                       val: any) -> None:
        """ method for setting new attribute value for agent """
        self.Attributes[attr] = val
    
    def get_attr_value(self,
                       attr: str) -> any:
        """ method for getting attribute value """
        return self.Attributes[attr]

# TODO: implement additional methods that return selections of agents based on rules, strategies, etc.
# TODO: Environment should not should support Array with agents, but should also provide access to a list of agents in the environment that can easily be iterated over; 
#       could also be a method that returns this list based on Array content
# TODO: Environment should also offer a method that allows an "update" of the database for a specified (input argument) simulation time (= iteration), so that this does not have to be implemented by the modeller
# environment class
class Environment:
    """ Environment can contain agents in cells """
    def __init__(self,
                capa_cell: int,
                endless: bool,
                rows: int,
                columns: int,
                db_manager: data.Manager
                ):
        """ constructs Environment instance, facilitating a grid for agent interactions """
        self.Cellcapacity = capa_cell # maximum amount of agents allowed to be in a cell
        self.Endless = endless        # whether grid is endless or has hard 2D borders
        self.Rows = rows
        self.Columns = columns
        self.Array = [[[] for j in range(columns)] for i in range(rows)]
        self.DBManager = db_manager
        self.DBManager.reset_table("environment")  
    
    def add_agent(self,
                  agent: Agent,
                  row: int = 0,
                  col: int = 0
                 ) -> None:
        """ method for adding agents to a cell in the grid; either a specific cell cna be specified, or, if one of the coordinates is not specified, a random cell is found and assigned """
        if row > 0 and col > 0:
            pass
        else:
            # randomly assign a row
            while True:
                #TODO: make this more computational efficient 
                row = random.choice(range(1,self.Rows+1))
                col = random.choice(range(1,self.Columns+1))
                if len(self.get_cell(row,col))< self.Cellcapacity: break
        
        self.Array[(row-1)][(col-1)].append(agent)
        agent.Row = row
        agent.Col = col
    
    def get_cell(self,
                 row: int,
                 col: int
                ) -> list:
        """ method for obtaining the agent list contained by the specified grid cell """
        return self.Array[(row-1)][(col-1)]
    
    def get_neighbourhood(self,
                          agent: Agent, # agent for which neighbourhood is to be identified
                          type: str,    
                          radius: int = 1,  
                          order: str = "random"
                         ) -> list:
        """ returns specified neighbourhood; type supports "moore", order supports "random" """
        ls_neighbourhood = []
        
        #TODO implement other neighbourhood orders, and other neighbourshood types --- 
        if "random" not in order: 
            order = "random"
            warning("currently only random order supported by get_neighbourhood, framework.py")
        
        if type == "moore":
            
            for row in range(agent.Row-radius,agent.Row+radius):
                for col in range(agent.Col-radius,agent.Col+radius):
                    if row == agent.Row and col == agent.Col:
                        # if cell capacity is greater than one then that means neighbourhood also includes the cell that the respective agent is located in
                        if self.Cellcapacity > 1:
                            if len(self.Array[row-1][col-1]) > 0:
                                
                                for o in self.Array[row-1][col-1]:
                                    if o == agent:
                                        pass
                                    else: 
                                        ls_neighbourhood.append(o) 
                    else:
                        if self.Endless == True:
                            if row < 1: row = self.Rows+row
                            if col < 1: col = self.Columns+col
                            if row > self.Rows: row = row - self.Rows
                            if col > self.Columns: col = col - self.Columns
                        if row >= 1 and row <= self.Rows and col >= 1 and col <= self.Columns:
                            for o in self.Array[row-1][col-1]:
                                ls_neighbourhood.append(o) 
        elif type == "neumann":
            #TODO implement neumann neighbourhood
            pass
        if order == "random":
            ls_neighbourhood = random.shuffle(ls_neighbourhood)
        else:
            #TODO implement additional ordering options
            pass
        
class Population: 
    """ Population class used for a single population, used by Populations class when adding populations """
    def __init__(self,
                 name: str,
                 size: int,
                 env: Environment,
                 id_lastused: int,
                 db_manager: data.Database,
                 attributes: list = [],
                 datatypes: list = [], # attribute datatypes (list of strings)
                 initialvals: list = [],
                 randomness: list = []):
        """ constructor for a population """
        self.Name = name
        self.Size = size
        self.Environment = env
        self.DBManager = db_manager
        self.Agents = {}

        # add to agent table the attribute columns
        if len(attributes) > len(datatypes) or len(attributes) < len(datatypes): warning("attributelist does not match datatypes list; when setting up Population")
        self.DBManager.add_agentcolumns(attributes, datatypes)

        # create agents one by one, add them to the environment, and add them to the dictionary
        for i in range(id_lastused+1, id_lastused+size+1):
            agent = Agent(i, self.Name)
            
            if len(attributes) > len(initialvals) or len(attributes) < len(initialvals): 
                warning("attributes list lenght does not match initialvals lengt; no attributes added in Population constructor")
            elif len(randomness) > 0 and len(randomness) > len(initialvals):
                warning("randomness list does not match initial value list")
            elif len(randomness) > 0 and len(randomness) < len(initialvals):
                warning("randomness list does not match initial value list")
            else:

                for j in range(0, len(attributes)):
                    # determine initial value
                    if len(randomness) > 0:
                        if randomness[j][0] == "uniform":
                            initialval = random.uniform(randomness[j][1]*initialvals[j], randomness[j][2]*initialvals[j])
                        elif randomness[j][0] == "normal":
                            initialval = random.gauss(randomness[j][1]*initialvals[j], randomness[j][2]*initialvals[j]) # randomness[j][1] represents scaling of mean; should normally be 1
                        else:
                            warning("in Population() constructor random distribution was not recognized; no randomn distribution applied")
                            initialval = initialvals[j]
                    else:
                        initialval = initialvals[j]
                    # add attribute and initial value
                    agent.add_attribute(attributes[j], initialval)
            
            # add agents to Agents dictionary
            self.Agents[agent.ID] = agent

            # add agent to environment
            self.Environment.add_agent(agent)

        # add column to environment table in database, with population as header (if not already added)
        self.DBManager.add_environmentcolumn(self.Name, "INTEGER") # for counting amount in that cell for that agent
    
    def get_agents(self) -> list:
        """ method for returning all agents of the population as a list """
        return list(self.Agents.values())
    
    def write_agents_to_db(self, 
                           simtime: int) -> None:
        """ method for writing all agents in population into database """
        if self.Size > 0:

            for agent in list(self.Agents.values()):
                self.DBManager.write_agentvalue(simtime, agent)

class Populations:
    """ Populations class for setting up and managing a population of agents """
    def __init__(self,
                 amount: int,
                 env: Environment,
                 db_manager: data.Manager):
        """ constructs population container, knowing the number of populations that will be added """
        self.Amount = amount
        self.Environment = env
        self.DBManager = db_manager
        self.ID_lastused = 0 # used for managing agent IDs in populations
        self.Populations = {}
        self.DBManager.reset_table("agents")  
    
    def add_population(self,
                       name: str,
                       size: int,
                       attributes: list = [],
                       datatypes: list = [], # list of strings, attribute datatypes
                       initialvals: list = [],
                       randomness: list = []):
        """ creates a population and adds it to the populations dictionary """
        self.Populations[name] = Population(name, size, self.Environment, self.ID_lastused, self.DBManager, attributes, datatypes, initialvals, randomness)
        self.ID_lastused += size

    def get_population(self,
                       name: str) -> Population:
        """ returns the specified population object from populations dictionary """
        return self.Populations[name]
    
    def reset_populations(self) -> None:
        """ method for resetting populations dictionary, deleting all old populations and resetting ID_lastused marker """
        if len(list(self.Populations.keys())) > 0:

            for key in list(self.Populations.keys()):
                del self.Populations[key]
        
        self.Populations = {}
        self.ID_lastused = 0
    
    def write_env_to_db(self, 
                        simtime: int) -> None:
        """ writes to db environment table in database with agent counts for population, for all agents in total and for the relevant population """
        
        vals = [0 for i in range(0,self.Amount)]

        for row in range(1,self.Environment.Rows+1):
            for col in range(1,self.Environment.Columns+1):

                # which population does each agent belong to? increment the respective column in the database
                self.DBManager.write_environmentcell(simtime, row, col, self.Environment, vals)
                self.DBManager.commit()

                list_cell = self.Environment.get_cell(row, col)

                if len(list_cell) > 0:

                    for agent in list_cell: 
                        self.DBManager.increment_envpop(simtime, row, col, agent.Population)
                        
    def write_agents_to_db(self,
                           simtime: int) -> None:
        """ writes to db all agents and their values """
        
        if self.Amount > 0:

            for key_pop in list(self.Populations.keys()):
                pop = self.Populations[key_pop]

                if pop.Size > 0:
                    
                    for key_agent in list(pop.Agents.keys()):
                        agent = pop.Agents[key_agent]

                        self.DBManager.write_agentvalue(simtime, agent)
    
    def update_db(self,
                  simtime: int) -> None:
        """ writes environment and all agent populations to database """
        self.write_env_to_db(simtime)
        self.write_agents_to_db(simtime)