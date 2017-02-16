# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 09:58:21 2017

@author: alysha.reinard
"""

import pyodbc
import numpy as np

def read_database():
    #connect to server
    server = 'XXX' 
    database = 'XXX' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+\
                      '; DATABASE='+database+'; Trusted_Connection=yes;')
    cursor = cnxn.cursor()

    #execute database call
    cursor.execute("SELECT TOP 10 * FROM [RA].[dbo].[ace_mag_1m] \
               where time_tag > '1998-02-17' and time_tag < '1998-02-18';")

    #get column names
    col_name = [column[0] for column in cursor.description]
    col_fmt = [column[1] for column in cursor.description]
    
    #return all rows from search
    all_rows = cursor.fetchall()

    #store in data structure
    data = np.array(all_rows, dtype = {'names': col_name, \
        'formats': col_fmt})
    
    cnxn.close
    
    print(data)