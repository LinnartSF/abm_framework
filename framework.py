"""

Module that provides a framework in the form of a class library that aids agent-based simulation modeling

The module only covers grid-based simulations

Classes comprise
- environment
- agent
- neighbourhood
- strategy

"""

__author__ = "Linnart Felkl"
__email__ = "linnartsf@gmail.com"

# environment class
class Environment:
    """ Environment can contain agents in cells """
    def __init__(self,
                capa_cell: int,
                endless: bool,
                rows: int,
                columns: int
                ):
        """ constructs Environment instance """
        self.Cellcapacity = capa_cell
        self.Endless = endless
        self.Rows = rows
        self.Columns = columns
        
