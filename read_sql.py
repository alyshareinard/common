# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 16:18:00 2016

@author: alyshareinard
"""
from sqlalchemy import create_engine
def read_sql():
    engine=create_engine('sqlite:///Chinook.sqlite')
    
# Save the table names to a list: table_names
table_names=engine.table_names()

# Print the table names to the shell
print(table_names)