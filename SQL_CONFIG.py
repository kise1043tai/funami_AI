#!/usr/bin/env python
# -*- coding:utf-8 -*-

# enable debugging

import pyodbc
import mysql.connector
class SQL_CONF():
    def __init__(self,server,database):
        self.server = server
        self.database = database
    def db_connection(self):    
        server = self.server
        database =  self.database
        username = 'mysql_admin_001'  
        password = 'PkNUHBc|U|5mtnPjLEQm~q+&,WHuE#c'  
        sv=server
        db=database
        un=username
        pw=password
        #cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+sv+';DATABASE='+db+';UID='+un+';PWD='+ pw)
        cnxn = mysql.connector.connect(user=un, password=pw, host=sv, database=db)
        return cnxn
    def db_connection_2(self):    
        server = self.server
        database =  self.database
        username = 'Admin'
        password = '0526250148'
        cnxn = pyodbc.connect('DRIVER={FileMaker ODBC};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        return cnxn