"""

Module that provides a framework in the form of a class library that aids agent-based simulation modeling

The module only covers grid-based simulations

Classes comprise
- environment
- agent

Module requires random module

"""

#TODO catch and handle infeasible user input
#TODO add additional typewriting to class atrributes

__author__ = "Linnart Felkl"
__email__ = "linnartsf@gmail.com"

# required modules
import random

# internal method for printing warnings
def warning(msg: str) -> None:
    print(f"WARNING: {msg}")

# agent class
class Agent:
    """ Agents have attributes that can be relevant to a simulation """
    def __init__(self,
                 attributes: list,  # list of strings (attribute names)
                 initialvals: list, # list of initial attribute values
                 ):
        # create a dictionary from the attributes and interavls, unless there are errors
        self.Attributes = None
        
        if len(attributes) == 0: 
            warning("Agent without attributes created")
        elif len(attributes) > len(initialvals) or len(attributes) < len(initialvals):
            warning("Agent attributes not created since initialvals length differs from attribute list lengths")
        else:
            self.Attributes = zip(attributes, initialvals)
            self.Row = 0 # represents unassigned
            self.Col = 0 # represents unassigned

# environment class
class Environment:
    """ Environment can contain agents in cells """
    def __init__(self,
                capa_cell: int,
                endless: bool,
                rows: int,
                columns: int
                ):
        """ constructs Environment instance, facilitating a grid for agent interactions """
        self.Cellcapacity = capa_cell # maximum amount of agents allowed to be in a cell
        self.Endless = endless        # whether grid is endless or has hard 2D borders
        self.Rows = rows
        self.Columns = columns
        self.Array = [[[] for j in range(columns)] for i in range(rows)]
    
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
                #TODO: make this more efficient so that it consumes less computational power
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
                          agent: Agent,
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
                        pass
                    else:
                        if self.Endless == True:
                            if row < 1: row = self.Rows+row
                            if col < 1: col = self.Columns+col
                            if row > self.Rows: row = row - self.Rows
                            if col > self.Columns: col = col - self.Columns
                        if row >= 1 and row <= self.Rows and col >= 1 and col <= self.Columns:
                            ls_neighbourhood.append(self.Array[row-1][col-1])
        elif type == "neumann":
            #TODO implement neumann neighbourhood
            pass
        if order == "random":
            ls_neighbourhood = random.shuffle(ls_neighbourhood)
        else:
            #TODO implement additional order options
            pass

# writing a small test
agent = Agent(["name"],["Linnart"])
env = Environment(1,False,3,3)
env.add_agent(agent,1,2)
print(env.Array)
print(env.get_neighbourhood(agent,"moore",2,"random"))