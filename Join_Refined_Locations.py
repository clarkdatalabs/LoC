'''
Created on Oct 26, 2017

@author: DJT
'''
import sqlite3
import pandas as pd
from geopy.geocoders import Nominatim
geolocator = Nominatim()

#import numpy as np

#df1 is has clustered and edited locations names in column subjectLocationRefined
df1 = pd.read_csv('subject_location_refined.csv')[['subjectLocation', 'subjectLocationRefined']]

#df2 will have one row per clustered location, and will have columns for longitude / latitude
df2 = df1[['subjectLocationRefined']].drop_duplicates()
df2.insert(0, 'locationID', range(1, 1 + len(df2)))

#print(len(df1), len(df2))
df3 = df2.head(5)

df3['loc']=df3['subjectLocationRefined'].map(lambda x: geolocator.geocode(x, addressdetails=True))

print(df3)



#for row in df2.head(5).iterrows():
#    print(row['subjectLocationRefined'])
    
    #location = geolocator.geocode(row["subjectLocationRefined"], addressdetails=True)
    #print(location)
    






def buildTables(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS Location (
                    locationID integer PRIMARY KEY,
                    locationName text,
                    long text,
                    lat text
                    )'''
      )
    
    c.execute('''CREATE TABLE IF NOT EXISTS Location_Refinement (
                    subjectLocation text,
                    locationID integer,
                    FOREIGN KEY (subjectLocation) REFERENCES Subject_Location(subjectLocation),
                    FOREIGN KEY (locationID) REFERENCES Location(locationID)
                    )'''
      )


    conn.commit()
    conn.close()

#set database to LoC
#db = 'LoC.db'


