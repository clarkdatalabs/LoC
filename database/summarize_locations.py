'''
This script extracts the summarized location_by_year.csv for use in the final visualization
'''

import sqlite3
import pandas as pd

db="LoC.db"
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
                           LEFT JOIN Location_2 l 
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

# create table of counts grouping by year and country
locationByYear = pd.read_sql_query('''SELECT 
                                 ISOnumeric3,
                                 ISOalpha2,
                                 ISOalpha3,
                                 countryName,
                                 pubDate, 
                                 COUNT(recordID) AS count
                             FROM 
                                 Book_Subject_Location
                             WHERE
                                 ISOnumeric3 IS NOT NULL
                             GROUP BY
                                 ISOnumeric3, pubDate ''', conn)

locationByYear.to_csv("../Visualization/location_by_year.csv", index=False)

conn.close()