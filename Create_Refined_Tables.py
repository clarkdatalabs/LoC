'''
Created on Oct 26, 2017

@author: DJT
'''
import sqlite3
import pandas as pd
import geocache
from sqlalchemy import create_engine
from geopy.geocoders import Bing


#df1 has clustered and edited locations names in column subjectLocationRefined
#df1 = pd.read_csv('ClusteringFiles/subject_location_refined.csv')

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



conn = sqlite3.connect(db)
c = conn.cursor()

#Build out Geocache table with any new entries
locations = c.execute('SELECT DISTINCT subjectLocationRefined FROM Subject_Location_Refined').fetchall()



cache = geocache.Cache("LoC.db")
if 1:
    i=0
    for locationTuple in locations:
        i+=1
        locationString = locationTuple[0]
        geoBLOB = cache.get_geoBLOB(locationString)
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
        c.execute('INSERT OR REPLACE INTO Location values (?,?,?,?,?)', (locationString, latitude, longitude, country, USAstate))
        conn.commit()
        if not i%10:
            print(i)

conn.commit()
conn.close()

#Extract all location fields from Geocache
conn = sqlite3.connect(db)
c = conn.cursor()

    


# c.execute('SELECT * FROM Geocache') 
# for row in c:
#     print(cache.location_cached(row[0])["address"])




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
    



