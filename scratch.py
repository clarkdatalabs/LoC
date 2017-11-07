subject = "Olympic Mountains (Wash.)"
failSubject = "Former Soviet republics"

#Nominatim
BingAPIkey = "AoHjJBfB_lnIWNP201cRJ70AItSb0hRGuIv2YvGpEOtUmDe41W9kghqEdUlZcMQz"

import sqlite3
import pandas as pd
import geocache
from geopy import geocoders

b = geocoders.Bing(BingAPIkey)
#n = geocoders.Nominatim()


# geoBLOB = b.geocode(query=failSubject,
#                     exactly_one=True,
#                     include_country_code=True)
#  
# print("query = ", geoBLOB)


cache = geocache.Cache("LoC.db")

sub1 = cache.get_geoBLOB(subject)
print("sub1:", sub1['point']['coordinates'][1])





# cacheBLOB = cache.location_cached(subject)
# 
# print("Is stored with data:",cache.location_cached(subject))
# 
# print("not a row:", cache.location_cached("not in the deck"))
# print("Failed subject:", cache.location_cached("Former Soviet republics"))
# 
# db="LoC.db"
# conn = sqlite3.connect(db)
# cur = conn.cursor()
# cur.execute('SELECT * FROM Geocache WHERE locationString=?', ("Former Soviet republics",))
# res = cur.fetchone()
# print("res =",res)



#print(bing.raw)
#print(bing.raw["address"]["countryRegionIso2"])


