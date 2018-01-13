'''
Created on Jan 12, 2018
@author: DJT

This script adds a new table Location Location_v2, to LoC.db.
This table is imported from Location_joined_cleaned.csv, which consists of 



'''
import sqlite3
import pandas as pd
from sqlalchemy import create_engine


db="../LoC.db"
conn = sqlite3.connect(db)
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS Location_2 (
               locationString STRING PRIMARY KEY, 
               latitude REAL, 
               longitude REAL, 
               ISOalpha2 TEXT, 
               USAstate TEXT
               )''')

conn.commit()
conn.close()

#save refined data to database
disk_engine = create_engine('sqlite:///../database/LoC.db')
pd.read_csv('Location_joined_cleaned.csv').to_sql('Location_2', disk_engine, if_exists='replace', index=False)


