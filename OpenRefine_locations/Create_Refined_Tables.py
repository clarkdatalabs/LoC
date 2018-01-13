'''
Created on Oct 26, 2017

@author: DJT
'''
import sqlite3
import pandas as pd
import geocache
from sqlalchemy import create_engine
from geopy.geocoders import Bing


db="../database/LoC.db"
conn = sqlite3.connect(db)
c = conn.cursor()

#Initialize Location table
#c.execute('DROP TABLE IF EXISTS Location')
#conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS Location (
               locationString STRING PRIMARY KEY, 
               latitude REAL, 
               longitude REAL, 
               ISOalpha2 TEXT, 
               USAstate TEXT
               )''')

c.execute('''CREATE TABLE IF NOT EXISTS Subject_Location_Refined (
                subjectLocation TEXT,
                subjectLocationRefined TEXT,
                FOREIGN KEY (subjectLocation) REFERENCES Subject_Location(subjectLocation),
                FOREIGN KEY (subjectLocationRefined) references Location(locationString)
                )'''
  )

conn.commit()
conn.close()

#save refined data to database
disk_engine = create_engine('sqlite:///LoC.db')
pd.read_csv('../OpenRefine_locations/subject_location_refined.csv').to_sql('Subject_Location_Refined', disk_engine, if_exists='replace', index=False)

#save country code and state code table to db
pd.read_csv('Countries.csv', encoding = "ISO-8859-1").to_sql('Countries', disk_engine, if_exists='replace', index=False)
pd.read_csv('USAstates.csv').to_sql('USAstates', disk_engine, if_exists='replace', index=False)

#------------------------#

#Build out Location table with any locations. Simultaneously builds Geocache table.
conn = sqlite3.connect(db)
c = conn.cursor()
locations = c.execute('SELECT DISTINCT subjectLocationRefined FROM Subject_Location_Refined').fetchall()

cache = geocache.Cache(db)

i=0
for locationTuple in locations:
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
                                l.ISOalpha2,
                                c.ISOalpha3,
                                c.countryName,
                                c.ISOnumeric3,
                                l.USAstate,
                                u.stateName
                      FROM 
                       (Subject_Location_Refined s 
                           LEFT JOIN Location l 
                               ON s.subjectLocationRefined = l.locationString)
                        LEFT JOIN Subject_Location t
                            ON t.subjectLocation = s.subjectLocation
                        LEFT JOIN Record r
                            ON r.recordID = t.recordID
                        LEFT JOIN Countries c
                            ON l.ISOalpha2 = c.ISOalpha2
                        LEFT JOIN USAstates u
                            ON l.USAstate = u.stateID
                WHERE c.ISOalpha3 IS NOT NULL
                ORDER BY r.pubDate
               ''') 
conn.commit()
conn.close()
   


