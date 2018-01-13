'''
This script extracts the summarized location_by_year.csv for use in the final visualization
'''

import sqlite3
import pandas as pd

print("blah 1")

db="LoC.db"
conn = sqlite3.connect(db)
c = conn.cursor()

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
print("blah 2")
conn.close()