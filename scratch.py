


subject = "Cambridge (Mass.)"

#Nominatim
BingAPIkey = "AoHjJBfB_lnIWNP201cRJ70AItSb0hRGuIv2YvGpEOtUmDe41W9kghqEdUlZcMQz"

import sqlite3
import pandas as pd
from geopy import geocoders

#g = geocoders.Google()
b = geocoders.Bing(BingAPIkey)
n = geocoders.Nominatim()

print(b)

bing = b.geocode(query=subject,
                exactly_one=True,
                include_country_code=True)

print(bing.raw)
print(bing.raw["address"]["countryRegionIso2"])

Nom = n.geocode(subject,
                exactly_one=True,
                addressdetails=True,
                polygon=True)
print(Nom.address, "\n", Nom.raw)

services = [b, n]
#for x in services:
#    for place, (lat, long) in x.geocode(subject):
        #print(x, place, lat, long)


#geolocator = Bing()
#location = geolocator.geocode(subject)
#print(location.address)
#print(location.longitude, location.latitude)
#print(location.raw)

#print(geolocator.geocode(subject, addressdetails=True, include_country_code=True))