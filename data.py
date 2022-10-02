"""

This script works with Python 3.10 and is meant to be called as an API from local Python installation

The module wraps pyodbc and sqlite3

"""

__author__ = "Linnart Felkl"
__email__ = "linnartsf@gmail.com"

import pyodbc
import sqlite3

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
            query = "DELETE FROM {};".format(tablename)
        else:
            query = "TRUNCATE TABLE {};".format(tablename)
        self.Cursor.execute(query)
    
    def delete_records(self,tablename: str, condition: str = "none") -> None:
        """ deletes all those entries from the datatable in which the condition is satisfied """
        query = "DELETE FROM {} WHERE {};".format(tablename,condition)
        self.Cursor.execute(query)
    
    def drop_table(self, tablename: str) -> None: 
        """ drops a table from the database, i.e. table is removed """
        self.Cursor.execute("DROP TABLE {};").format(tablename)