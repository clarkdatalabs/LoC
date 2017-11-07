'''
Created on Oct 26, 2017

@author: DJT
'''





import sqlite3
import pandas as pd
import geocache
from sqlalchemy import create_engine
import pprint
#import numpy as np



#df1 has clustered and edited locations names in column subjectLocationRefined
#df1 = pd.read_csv('ClusteringFiles/subject_location_refined.csv')

db="LoC.db"
conn = sqlite3.connect(db)
c = conn.cursor()

#Initialize Location table
c.execute('''CREATE TABLE IF NOT EXISTS Location (
               locationString STRING PRIMARY KEY, 
               longitude REAL, 
               Latitude REAL, 
               Country TEXT, 
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

#define geocoder
from geopy.geocoders import Bing
BingAPIkey = "AoHjJBfB_lnIWNP201cRJ70AItSb0hRGuIv2YvGpEOtUmDe41W9kghqEdUlZcMQz"
geolocator = Bing(BingAPIkey)

conn = sqlite3.connect(db)
c = conn.cursor()

#Build out Geocache table with any new entries
locations = c.execute('SELECT DISTINCT subjectLocationRefined FROM Subject_Location_Refined').fetchall()


cache = geocache.Cache("LoC.db")
i = 0
for locationTuple in locations[0:1000]:
    i+=1
    locationString = locationTuple[0]
    geoBLOB = cache.location_cached(locationString)
    if geoBLOB:
        print('\'', locationString, '\' geocoding was retrieved from cache', sep='')
    else:
        #print('\'', locationString, '\' was not cached, looking up and caching now')
        geoBLOB = geolocator.geocode(locationString)
        cache.save_to_cache(locationString, geoBLOB)
        #print('... and now cached.')
    if not i%10:
        print(i)
    
     


conn.commit()
conn.close()



#df2 will have one row per clustered location, and will have columns for longitude / latitude
#df2 = df1[['subjectLocationRefined']].drop_duplicates()



#df2.insert(0, 'locationID', range(1, 1 + len(df2)))

#print(len(df1), len(df2))


#df3 = df2.head(5)

#for row in df3.iterrows():
#    print(row[1][1])




#df3['loc']=df3['subjectLocationRefined'].map(lambda x: geolocator.geocode(x, addressdetails=True))

#print(df3["loc"])



#for row in df2.head(5).iterrows():
#    print(row['subjectLocationRefined'])
    
    #location = geolocator.geocode(row["subjectLocationRefined"], addressdetails=True)
    #print(location)
    



