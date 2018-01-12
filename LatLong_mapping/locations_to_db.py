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



