"""

This script works with Python 3.10 and is meant to be called as an API from local Python installation

The module wraps pyodbc and sqlite3

This package assumes a slite database (in future mssql will be supported in an extension of this package)

Data.py furthermore assumes, that the database has the following tables 
- agents: 
   contains one fixed column "simtime", for storing simulation time
   additional columns must be added for each new simulation application; 
   table contains data on agents states throughout simulation times, i.e. relevant properties of the agent
- environment: 
   predefined fixed column names (columns)
   column simtime - simulation time
   column row - row index
   column col - column index
   column agents - agent count registered in the cell
   additional columns can be added

This module provides a Database class to connect to the database and to perform database operations.

This module provides a Manager class that standardizes e.g. column addition to table, state registration in agent table, etc.

Developers can add onto the Manager class or use the Database class to directly facilitate custom queries.

"""

#TODO add type writing to classes
#TODO improve type writing of method calls, specifying agent datatype for input parameter
#TODO catch errors results from faulty user input (e.g. column datatype for new column, etc.)

__author__ = "Linnart Felkl"
__email__ = "linnartsf@gmail.com"

import pyodbc
import sqlite3
from framework import *

def warning(msg: str) -> None: 
    print("WARNING: "+msg)

class Database: 
    """ this class can be used to establish a database connection with pyodbc or just directly with sqlite3 """
    def __init__(self, type: str, db: str, server: str = "") -> None:
        """ constructor """
        self.Server = server
        self.Name = db
        self.Type = type
        if type == "sqlite3":
            self.Connection = sqlite3.connect(db+".db")
        elif type == "pyodbc":
            self.Connection = pyodbc.connect("DRIVER={SQL Server};SERVER="+server+";DATABASE="+db+";Trusted_connection=yes")
        else:
            warning("Database of unknown type was requested!")
        self.Cursor = self.Connection.cursor()
    
    def connect(self) -> None:
        """ establishes connection, e.g. if connection is closed and then opened again """
        if self.Type == "sqlite3":
            self.Connection = sqlite3.connect(self.Name+".db")
        elif self.Type == "pyodbc":
            self.Connection = pyodbc.connect("DRIVER={SQL Server};SERVER="+self.Server+";DATABASE="+self.Name+";Trusted_connection=yes")
        else:
            warning("connect() in database class does not recognize database type")
        self.Cursor = self.Connection.cursor()
    
    def query(self, query: str)-> None:
        """ executes specified query on database """
        self.Cursor.execute(query)
    
    def read(self,x: int) -> list:
        """ returns specified amount of rows from query execution (cursor obj) 
        input paramter x: 1 == return one data row, x > 1 return x data rows, otherwise return all rows """
        if x == 1:
            return self.Cursor.fetchone()
        elif x > 1:
            return self.Cursor.fetchmany(x)
        else:
            return self.Cursor.fetchall()
    
    def commit(self)-> None:
        """ commits changes without closing connection to database """
        self.Connection.commit()
    
    def close(self) -> None:
        """ closes connection to database without committing """
        self.Connection.close()
    
    def commit_n_close(self) -> None:
        """ perform commit and then close database connection """
        self.Connection.commit()
        self.Connection.close()
    
    def truncate_table(self, tablename: str) -> None:
        """ deletes all records and data in the table """
        if self.Type == "sqlite3":
            query = f"DELETE FROM {tablename};"
        else:
            query = f"TRUNCATE TABLE {tablename};"
        self.Cursor.execute(query)
    
    def delete_records(self,tablename: str, condition: str = "none") -> None:
        """ deletes all those entries from the datatable in which the condition is satisfied """
        query = f"DELETE FROM {tablename} WHERE {condition};"
        self.Cursor.execute(query)
    
    def drop_table(self, tablename: str) -> None: 
        """ drops a table from the database, i.e. table is removed """
        self.Cursor.execute(f"DROP TABLE {tablename};")
    
class Manager:
    """ this class provides an interface for standardized database operations relevant to ABM simulation conducted with this package """
    def __init(self,
               db: Database) -> None:
        """ constructor of Manager instance """
        self.Database = db
    
    def add_column(self,
                   colname: str,
                   coltype: str,
                   table: str) -> None:
        """ method for adding column to specified table; WARNING: does not commit after querying! """
        self.Database.query(f"ALTER TABLE {table} ADD {colname} {coltype};")
        self.Database.commit()

    def add_agentcolumn(self,
                        colname: str,
                        coltype: str) -> None:
        """ method for adding a column to agent table in results database """
        self.add_column(colname, coltype, "agents")
        self.Database.commit()
    
    def add_agentcolumns(self, 
                         colnames: list,
                         coltypes: list) -> None:
        """ method for adding several columns to agent tabel in results database """
        if len(colnames) == len(coltypes):
            for i in range(0,len(colnames)):
                self.add_column(colnames[i],coltypes[i],"agents")
            self.Database.commit()
        else:
            warning("no columns added to agent table since coltypes length doesnt matches colnames length")
    
    def add_environmentcolumn(self, 
                              colname: str,
                              coltype: str) -> None:
        """ method for adding colum to environment table in results database """
        self.add_column(colname, coltype, "environment")
        self.Database.commit()
    
    def add_environmentcolumns(self,
                               colnames: list,
                               coltypes: list) -> None:
        """ method for adding several methods to environment table in results database """
        if len(colnames) == len(coltypes):
            for i in range(0,len(colnames)):
                self.add_column(colnames[i], coltypes[i], "environment")
            self.Database.commit()
        else: 
            warning("no columns added to environment table since lengths of col names and col types list dont match")

    def remove_column(self,
                      colname: str,
                      table: str) -> None:
        """ removes specified column from specified table; WARNING does not commit query """
        self.Database.query(f"ALTER TABLE {table} DROP COLUMN {colname};")
        self.Database.commit()

    def remove_agentcolumn(self,
                           colname: str) -> None:
        """ removes specified column from agents table and commits change """
        self.remove_column(colname, "agents")
        self.Database.commit()

    def remove_agentcolumns(self,
                            colnames: list) -> None:
        """ removes specified column names from agents table and commits changes """
        for col in colnames:
            self.remove_column(col, "agents")
        self.Database.commit()

    def remove_environmentcolumn(self,
                                 colname: str) -> None:
        """ removes specified column from environment table and commits change """
        self.remove_column(colname, "environment")
        self.Database.commit()

    def remove_environmentcolumns(self, 
                                  colnames: list) -> None:
        """ removes specified columns from environment table and commits changes """
        for col in colnames:
            self.remove_column(col, "environment")
        self.Database.commit()

    def reset_table(self,
                    table: str) -> None:
        """ deletes any columns that might have been added in excess of the default columns """
        self.query(f"SELECT name FROM PRAGMA_TABLE_INFO('{table}');");
        df = self.read(-1)
        #TODO ierate over column headers, and drop the columns
    
    def reset_tables(self) -> None:
        """ deleltes any columns that might have been added in excess of default, in agents and environment tables """
        # TODO
        pass

    def write_agentvalue(self,
                         simtime: int,
                         agent: Agent) -> None:
        """ for the given agent, attribute values are written into database for the respective simulation time """
        attributestr = ",".join([str(i) for i in agent.Attributes.values()])
        valuestr = str(simtime),",",attributestr
        self.Database.query(f"INSERT INTO agents VALUES({valuestr});")
        self.Database.commit()
        
    def write_agentstates(self,
                          simtime: int,
                          agents: list) -> None:
        """ method writes attributes values of all agents in list into database, for specified simtime """
        # TODO
        pass

    def write_environmentstate() -> None:
        """ description """
        # TODO
        pass
    
    def close(self) -> None:
        """ closes Database connection """
        self.Database.close()

#  testing
import config
db = Database("sqlite3", config.path_databasefile)
db.query("SELECT name FROM PRAGMA_TABLE_INFO('environment');")
result = [i[0] for i in db.read(-1)]
print(str(result))