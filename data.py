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
import pandas

def warning(msg: str) -> None: 
    print("WARNING: "+msg)

# TODO - consider merging Database and Manager class, to only have Database class
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

    @staticmethod
    def vals_to_str(vals: list) -> str:
        """ method for converting a list of values into a SQLite friendly query strings """
        print("inside vals_to_str: "+str(vals))
        returnstr = ""
        for i in vals:
            if type(i) == str: 
                returnstr = returnstr+",'"+i+"'"
            else:
                if len(returnstr)>0:
                    returnstr = returnstr+","+str(i)
                else:
                    returnstr = str(i)
        return returnstr
    
class Manager:
    """ this class provides an interface for standardized database operations relevant to ABM simulation conducted with this package """
    def __init__(self,
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
    
    def add_agentcolumns(self, 
                         colnames: list,
                         coltypes: list) -> None:
        """ method for adding several columns to agent tabel in results database """
        if len(colnames) == len(coltypes):
            for i in range(0,len(colnames)):
                self.add_column(colnames[i],coltypes[i],"agents")
        else:
            warning("no columns added to agent table since coltypes length doesnt matches colnames length")
    
    def add_environmentcolumn(self, 
                              colname: str,
                              coltype: str) -> None:
        """ method for adding colum to environment table in results database """
        self.add_column(colname, coltype, "environment")
    
    def add_environmentcolumns(self,
                               colnames: list,
                               coltypes: list) -> None:
        """ method for adding additional columns to environment table in results database, in excess of default """
        if len(colnames) == len(coltypes):
            for i in range(0,len(colnames)):
                self.add_column(colnames[i], coltypes[i], "environment")
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

    def remove_agentcolumns(self,
                            colnames: list) -> None:
        """ removes specified column names from agents table and commits changes """
        for col in colnames:
            self.remove_column(col, "agents")

    def remove_environmentcolumn(self,
                                 colname: str) -> None:
        """ removes specified column from environment table and commits change """
        self.remove_column(colname, "environment")

    def remove_environmentcolumns(self, 
                                  colnames: list) -> None:
        """ removes specified columns from environment table and commits changes """
        for col in colnames:
            self.remove_column(col, "environment")

    def reset_table(self,
                    table: str) -> None:
        """ deletes any old data in table first, and then any columns that might have been added in excess of the default columns """
        self.Database.truncate_table(table)
        self.Database.commit()
        self.Database.query(f"SELECT name FROM PRAGMA_TABLE_INFO('{table}');")
        colnames = [i[0] for i in self.Database.read(-1)]
        for colname in colnames:
            if table == "agents":
                if colname in ["simtime","id"]:
                    # dont drop because default column
                    pass
                else:
                    # drop column because not a default column
                    self.remove_column(colname, "agents")
            elif table == "environment":
                if colname in ["simtime","row","col","agents"]:
                    # dont drop because default column
                    pass
                else:
                    # drop because it is not a default column
                    self.remove_column(colname, "environment")
            else:
                warning("unknown table forwarded to reset_table; nothing was reset for this Manager reset_table() method call")
    
    def reset_tables(self) -> None:
        """ deletes any columns that might have been added in excess of default, in agents and environment tables """
        self.reset_table("agents")
        self.reset_table("environment")
    
    # TODO: specify setup functions here for setting up agent table with specified columns, environment table with specifed columns, and population (environment extensions); 
    #       setting up population will check whether database has already been setup for environment, and if not, will do so; otherwise will just add coluns for counting agents per population

    # TODO: add option of only writing into certain column, specified by column name
    def write_to_table(self,
                       table: str,
                       vals: list) -> None:
        """ function writes vals into specified table, assuming vals string specifies values for every column in the table """
        valuestr = self.Database.vals_to_str(vals)
        self.Database.query(f"INSERT INTO {table} VALUES({valuestr});")
        self.Database.commit()

    def write_agentvalue(self,
                         simtime: int,
                         agent: Agent) -> None:
        """ for the given agent, attribute values are written into database for the respective simulation time """
        ATT = agent.Attributes
        print("ATT:")
        print(ATT)
        lsAttr = list(ATT.values())
        print("lsAttr:")
        print(str(lsAttr))
        db = self.Database
        strAttr = db.vals_to_str(lsAttr)
        print("strAttr:")
        print(strAttr)
        
        # old logic
        # valuestr = str(simtime),",",str(agent.ID),",",self.Database.vals_to_str(list(agent.Attributes.values()))

        # new logic
        valuestr = str(simtime),",",str(agent.ID),",",strAttr
        print("valuestr:")
        print(valuestr)

        self.Database.query(f"INSERT INTO agents VALUES({valuestr});")
        self.Database.commit()
        
    def write_agentvalues(self,
                          simtime: int,
                          agents: list) -> None:
        """ method writes attributes values of all agents in list into database, for specified simtime """
        for agent in agents:
            self.write_agentvalue(simtime, agent)

    def write_environmentcell(self,
                              simtime: int,
                              row: int,
                              col: int,
                              env: Environment,
                              vals: list = []) -> None:
        """ writes specified list of values into environment table, for the specified simulation time and cell """
        valuestr = str(simtime),",",str(row),",",str(col),",",str(len(env.Array[row-1][col-1]))
        if len(vals)>0: valuestr = valuestr,self.Database.vals_to_str(vals)
        self.Database.query(f"INSERT INTO environment VALUES({valuestr});")
        self.Database.commit()
    
    def close(self) -> None:
        """ closes Database connection """
        self.Database.close()
    
    def get_agentsdf(self, 
                     condition: str = "none") -> pandas.DataFrame:
        """ returns agent table as pandas dataframe; optional filtering condition """
        if condition == "none":
            # return entire table
            return pandas.read_sql_query("SELECT * FROM agents", self.Database.Connection)
        else:
            # return only those rows that satisfy the condition
            return pandas.read_sql_query(f"SELECT * FROM agents WHERE {condition}", self.Database.Connection)

    def get_environmentdf(self, 
                          condition: str = "none") -> pandas.DataFrame:
        """ returns environment table as pandas dataframe; optional filtering condition """
        if condition == "none":
            # return entire table
            return pandas.read_sql_query("SELECT * FROM environment", self.Database.Connection)
        else:
            # return only those rows that satisfy the condition
            return pandas.read_sql_query(f"SELECT * FROM environment WHERE {condition}", self.Database.Connection)
    
    def get_df(self,
               table: str,
               condition: str = "none") -> pandas.DataFrame:
        """ returns either agent or environment table as pandas dataframe, optional filtering """
        if table == "agents":
            return self.get_agentsdf(condition)
        elif table == "environment":
            return self.get_environmentdf(condition)
        else:
            warning("unknown table name as argument for get_df in data.py; returned None")
            return None