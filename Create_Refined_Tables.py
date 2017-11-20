'''
Created on Oct 26, 2017

@author: DJT
'''
import sqlite3
import pandas as pd
import geocache
from sqlalchemy import create_engine
from geopy.geocoders import Bing


db="LoC.db"
conn = sqlite3.connect(db)
c = conn.cursor()

#Initialize Location table
c.execute('''CREATE TABLE IF NOT EXISTS Location (
               locationString STRING PRIMARY KEY, 
               latitude REAL, 
               longitude REAL, 
               country TEXT, 
               USAstate TEXT
               )''')

c.execute('''CREATE TABLE IF NOT EXISTS Subject_Location_Refined (
                recordID integer,
                subjectLocation TEXT,
                subjectLocationRefined TEXT,
                FOREIGN KEY (recordID) REFERENCES Record(recordID),
                FOREIGN KEY (subjectLocationRefined) references Location(locationString)
                )'''
  )

conn.commit()
conn.close()

#save refined data to database
disk_engine = create_engine('sqlite:///LoC.db')
pd.read_csv('ClusteringFiles/subject_location_refined.csv').to_sql('Subject_Location_Refined', disk_engine, if_exists='replace', index=False)

#save country code and state code table to db
pd.read_csv('Countries.csv').to_sql('Countries', disk_engine, if_exists='replace', index=False)
pd.read_csv('USAstates.csv').to_sql('USAstates', disk_engine, if_exists='replace', index=False)

#------------------------#

#Build out Locations table with any locations. Simultaneously builds Geocache table.
conn = sqlite3.connect(db)
c = conn.cursor()
locations = c.execute('SELECT DISTINCT subjectLocationRefined FROM Subject_Location_Refined').fetchall()

cache = geocache.Cache("LoC.db")

i=0
for locationTuple in locations[0:2]:
    i+=1
    locationString = locationTuple[0]
    #get the geoBLOB to parse
    geoBLOB = cache.get_geoBLOB(locationString)
    
    #Parse out each of the required fields. Default to None on error.
    try: 
        latitude = geoBLOB['point']['coordinates'][0]
    except: latitude = None
    try: longitude = geoBLOB['point']['coordinates'][1]
    except: longitude = None
    try: 
        country = geoBLOB["address"]["countryRegionIso2"]
    except: country = None
    USAstate = None
    if country == "US":
        try: 
            USAstate = geoBLOB["address"]["adminDistrict"]
        except: pass
        
    #insert or replace the row in Location table
    c.execute('INSERT OR REPLACE INTO Location values (?,?,?,?,?)', (locationString, latitude, longitude, country, USAstate))
    conn.commit()
    
    #print counter every 10 locations
    if not i%10:
        print(i)

conn.commit()
conn.close()
   

#construct View with location and record data in one table
conn = sqlite3.connect(db)
c = conn.cursor()

c.execute('DROP VIEW IF EXISTS Book_Subject_Location')
conn.commit()

#Create View with one row per subject location (sometimes multiple per record)
c.execute('''CREATE VIEW Book_Subject_Location AS 
               SELECT DISTINCT  r.recordID,
                                r.pubDate,
                                l.country,
                                l.USAstate,
                                c.countryName,
                                u.stateName
                      FROM 
                       (Subject_Location_Refined s 
                           LEFT JOIN Location l 
                               ON s.subjectLocationRefined = l.locationString)
                        LEFT JOIN Record r
                            ON r.recordID = s.recordID
                        LEFT JOIN Countries c
                            ON l.country = c.countryID
                        LEFT JOIN USAstates u
                            ON l.USAstate = u.stateID
                WHERE l.country IS NOT NULL
                ORDER BY r.pubDate
               ''') 
conn.commit()
conn.close()
   


