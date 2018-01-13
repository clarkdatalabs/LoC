'''
Created on Dec 8, 2017

This script queries for all unique locations strings in the
Subject_Location table in LoC.db. These are the all of the raw, unprocessed
subject locations (MARC 650a) identified in the LoC records

@author: DJT
'''

import sqlite3
import pandas as pd
from sqlalchemy import create_engine


db="../database/LoC.db"
conn = sqlite3.connect(db)
c = conn.cursor()

disk_engine = create_engine('sqlite:///LoC.db')

SQL = '''SELECT 
            subjectLocation 
        FROM 
            Subject_Location
        GROUP BY
            subjectLocation
'''

#create table aggregating all years together
subjectLocation = pd.read_sql_query(SQL, conn)
                                 
subjectLocation.to_csv("subject_location.csv", index = False)

conn.close()