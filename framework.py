"""

Module that provides a framework in the form of a class library that aids agent-based simulation modeling

The module only covers grid-based simulations

Classes comprise
- environment
- agent

Module requires random module

"""

# TODO support other query languages than SQLite (where differences apply)
# TODO implement Distribution class

__author__ = "Linnart Felkl"
__email__ = "linnartsf@gmail.com"

# required modules
import random
import data

def warning(msg: str) -> None:
    """ internal but also externally accessible function for printing warning message (used for faulty user input) """
    print(f"WARNING: {msg}")

# simulation class
class Simulation:
    """ Simulation is running or not, and has iteration counter and a max iteration limit """

    Running: bool
    Iteration: int
    Limit: int

    def __init__(self,
                 limit: int):
        """ constructor for a new simulation instance """
        self.Running = True
        self.Iteration = 0
        self.Limit = limit
    
    def run(self) -> bool:
        """ method for incrementing simulation iteration; also sets running to False to avoid another simulation run in a endless while loop; returns boolean for whether simulation still runs another iteration """
        self.Iteration += 1
        if self.Iteration >= self.Limit: self.Running = False
        if self.Iteration <= self.Limit:
            return True
        else:
            return False

# agent class
class Agent:
    """ Agents have attributes that can be relevant to a simulation """

    ID: int
    Population: str
    Row: int
    Col: int
    Attributes: dict

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

    Cellcapacity: int
    Endless: bool
    Rows: int
    Columns: int
    Array: list
    Freecells: list
    DBManager: data.Manager

    def __init__(self,
                capa_cell: int,
                endless: bool,
                rows: int,
                columns: int,
                db_manager # data.Manager
                ):
        """ constructs Environment instance, facilitating a grid for agent interactions """
        self.Cellcapacity = capa_cell # maximum amount of agents allowed to be in a cell
        self.Endless = endless        # whether grid is endless or has hard 2D borders
        self.Rows = rows
        self.Columns = columns
        self.Array = [[[] for j in range(columns)] for i in range(rows)]
        self.Freecells = [(row,col) for row in range(1,rows+1) for col in range(1,columns+1)]
        self.DBManager = db_manager
        self.DBManager.reset_table("environment")  
    
    def add_agent(self,
                  agent: Agent,
                  row: int = 0,
                  col: int = 0
                 ) -> None:
        """ method for adding agents to a cell in the grid; either a specific cell that can be specified, or, if one of the coordinates is not specified, a random cell is found and assigned """
        
        if len(self.Freecells) <= 0:
            
            warning("no free cells in environment, add_agent() in framework.py did not add agent to grid")
            return None

        if row > 0 and col > 0:
            
            if (row,col) in self.Freecells:
                self.Freecells.remove((row,col))
            else:
                warning("add_agent() in framework.py wants to place agent in cell that is not free; did not add agent")
                return None

        else:

            cell = self.Freecells.pop(random.randint(0,len(self.Freecells)-1))
            row = cell[0]
            col = cell[1]
            
        self.Array[(row-1)][(col-1)].append(agent)
        agent.Row = row
        agent.Col = col

        if len(self.Array[(row-1)][(col-1)]) < self.Cellcapacity: 
            self.Freecells.append(cell)
    
    def get_freecells(self) -> list:
        """ method for returning index list for all empty cells """
        return self.Freecells
    
    def get_freecell(self,
                    row: int,
                    col: int,
                    targetcell: bool = False,
                    radius: int = -1,
                    ) -> tuple:
        """ gets a free cell randomly, either from entire grid or as close to specified cell as possible; if radius is set, return None if no free cell found, otherwise tuple """
        
        if radius >= min([self.Columns,self.Rows])/2: 
            warning("infeasible radius in get_freecell; radius reset by get_freecell in framework.py")
            
            if self.Columns > 2 and self.Rows > 2:
                radius = (min([self.Columns,self.Rows])-1)/2
            
            else:
                warning("grid is not big enough for even a small radius of 1; get_freecell in framework.py returns None")
                return None
        
        if len(self.Freecells) == 0: return None

        if radius == -1:
            if len(self.Freecells)>0:
                return random.choice(self.Freecells)

        else:
            startidx = 1
            if targetcell == True: startidx = 0

            for i in range(startidx,radius+1):
                neighbours = []
                    
                x = row-1-i
                if x < 0 and self.Endless == True: x = self.Rows-1+x

                y = col-1-i
                if y < 0 and self.Endless == True: y = self.Columns-1+y

                if x >= 0 and y >= 0:
                    if len(self.Array[x][y]) < self.Cellcapacity: neighbours.append((x,y))

                x = row-1+i
                if x > self.Rows-1 and self.Endless == True: x = x - (self.Rows-1)

                y = col-1+i
                if y > self.Columns-1 and self.Endless == True: y = y - (self.Columns-1)
                
                if x < self.Rows and y < self.Columns:
                    if len(self.Array[x][y]) < self.Cellcapacity: neighbours.append((x,y))

                if len(neighbours) > 0:
                    return random.choice(neighbours)

        return None

    def update_freecells(self) -> None:
        """ method for checking all free cells, and if they are occupied by now, remove cell from list of free cells  """
        for rowidx in range(self.Rows):
            for colidx in range(self.Columns):

                if len(self.Array[rowidx][colidx]) >= self.Cellcapacity: self.Freecells.remove(rowidx+1,colidx+1)

    def update_freecell(self,
                        row: int,
                        col: int
                       ) -> None:
        """ description """
        if len(self.Array[(row-1)][(col-1)]) >= self.Cellcapacity: self.Freecells.remove((row,col))
         
    def get_cell(self,
                 row: int,
                 col: int
                ) -> list:
        """ method for obtaining the agent list contained by the specified grid cell """
        return self.Array[(row-1)][(col-1)]
    
    def get_neighbourhood(self,
                          agent: Agent, # calling agent for which neighbourhood is to be identified
                          type: str = "moore",    
                          radius: int = 1,  
                          order: str = "random"
                         ) -> list:
        """ returns specified neighbourhood in the form of a list of all agents in the neighbourhood, except the calling agent itself; type supports "moore", order supports "random" """
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
            random.shuffle(ls_neighbourhood)
        else:
            #TODO implement additional order options
            pass
        
        return ls_neighbourhood
        
class Population: 
    """ Population class used for a single population, used by Populations class when adding populations """

    Name: str
    Size: int
    Environment: Environment
    DBManager: data.Manager
    Attributes: list
    Datatypes: list
    Initialvals: list
    Agents: dict

    def __init__(self,
                 name: str,
                 size: int,
                 env: Environment,
                 id_lastused: int,
                 db_manager, #data.Manager,
                 attributes: list = [],
                 datatypes: list = [], # attribute datatypes (list of strings)
                 initialvals: list = [],
                 randomness: list = []):
        """ constructor for a population """
        self.Name = name
        self.Size = size
        self.Environment = env
        self.DBManager = db_manager
        self.Attributes = attributes
        self.Datatypes = datatypes
        self.Initialvals = initialvals
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
    
    def get_agents(self, 
                   n: int = -1
                  ) -> list:
        """ method for returning all agents of the population as a list """
        if n < 0:
            
            # return all
            return list(self.Agents.values())
        
        else:

            # randomly select n agents to return in a list
            ls_all = list(self.Agents.values())
            ls_return = []
            if self.Size < n: n = self.Size
            for _ in range(n):
                idx = random.randint(0,(len(ls_all)-1))
                ls_return.append(ls_all.pop(idx))
            
            # return the random sample
            return ls_return

    def write_agents_to_db(self, 
                           simtime: int) -> None:
        """ method for writing all agents in population into database """
        if self.Size > 0:

            for agent in list(self.Agents.values()):
                self.DBManager.write_agentvalue(simtime, agent)

class Populations:
    """ Populations class for setting up and managing a population of agents """

    Amount: int
    Environment: Environment
    DBManager: data.Manager
    Attributes: list
    Datatypes: list
    ID_lastused: int
    Populations: dict

    def __init__(self,
                 amount: int,
                 env: Environment,
                 db_manager, # data.Manager
                 attributes: list,
                 datatypes: list
                ):
        """ constructs population container, knowing the number of populations that will be added """
        self.Amount = amount
        self.Environment = env
        self.DBManager = db_manager
        self.Attributes = attributes
        self.Datatypes = datatypes

        self.ID_lastused = 0 # used for managing agent IDs in populations
        self.Populations = {}

        self.DBManager.reset_table("agents")
        self.DBManager.reset_table("density")
        for i in range(0,len(datatypes)):
            if datatypes[i] in ["REAL","INTEGER"]: self.DBManager.add_densitycolumn(attributes[i])
    
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
                self.DBManager.write_environmentcell(simtime, row, col, vals)
                self.DBManager.commit()

                list_cell = self.Environment.get_cell(row, col)

                if len(list_cell) > 0:

                    for agent in list_cell: 
                        self.DBManager.increment_envpop(simtime, row, col, agent.Population)
    
    def write_density_to_db(self, 
                            simtime: int) -> None:
        """ writes to db density table in database with agent property accumulation where relevant """
        if self.Amount > 0:
            
            vals = set()
            for key_pop in list(self.Populations.keys()):
                pop = self.Populations[key_pop]

                for i in range(0,len(pop.Datatypes)):
                    if pop.Datatypes[i] in ["INTEGER","REAL"]:
                        vals.add(pop.Attributes[i])
            vals = list(vals)
            vals = [0.0 for i in vals]
            
            for row in range(1, self.Environment.Rows+1):
                for col in range(1,self.Environment.Columns+1):

                    self.DBManager.write_densitycell(simtime, row, col, vals)
                    self.DBManager.commit()

                    list_cell = self.Environment.get_cell(row, col)

                    if len(list_cell) > 0:

                        for agent in list_cell:
                            attr_keys = list(agent.Attributes.keys())
                            attr_vals = list(agent.Attributes.values())
                            for i in range(0, len(attr_vals)):

                                if type(attr_vals[i]) == float or type(attr_vals[i]) == int:
                                    self.DBManager.increase_density(simtime, row, col, attr_keys[i], attr_vals[i])
                        
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
        self.write_density_to_db(simtime)