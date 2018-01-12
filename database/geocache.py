
#import geopy
import pickle
import sqlite3
from geopy.geocoders import Bing

class Cache(object):
    def __init__(self, fn='LoC.db'):
        self.conn = conn = sqlite3.connect(fn)
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS '
                   'Geocache ( '
                   'locationString STRING PRIMARY KEY, '
                   'geoBLOB BLOB '
                   ')')
        conn.commit()

    def location_cached(self, locationString):
        #Returns False if no row exists for locationString
        #Returns None if a row exists for locationString, but no geoBLOB was returned from the geocoder for this string
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM Geocache WHERE locationString=?', (locationString,))
        res = cur.fetchone()
        #res == None if no row was found for locationString 
        if res == None: return False
        return pickle.loads(res[1])

    def save_to_cache(self, locationString, geoBLOB):
        #if the returned geoBLOB is populated, store a flattened version of the .raw result
        if not geoBLOB == None:
            geoBLOB = geoBLOB.raw
        cur = self.conn.cursor()
        cur.execute('INSERT INTO Geocache(locationString, geoBLOB) VALUES(?, ?)',
                    (locationString, sqlite3.Binary(pickle.dumps(geoBLOB, -1))))
        self.conn.commit()
        return(geoBLOB)
        
    def get_geoBLOB(self, locationString, geolocator = Bing("AoHjJBfB_lnIWNP201cRJ70AItSb0hRGuIv2YvGpEOtUmDe41W9kghqEdUlZcMQz")):
        try:
            #first check cache for geoBLOB
            geoBLOB = self.location_cached(locationString)
            #if no row found, call geocoder and save results to cache
            if geoBLOB == False:
                print("querying: \'", locationString, "\'", sep='')
                geoBLOB = geolocator.geocode(query = locationString.translate({ord(c): None for c in '<>'}), #<> cause errors in Bing
                                             exactly_one=True,
                                             include_country_code=True)
                geoBLOB = self.save_to_cache(locationString, geoBLOB)
            return(geoBLOB)
        except Exception as inst:
            print("ERROR: For locationString = \'",locationString,"\', the following error was encountered: ", inst, sep='')
            

  
  
        
if __name__ == '__main__':
    # run a small test in this case
    import pprint
    BingAPIkey = "AoHjJBfB_lnIWNP201cRJ70AItSb0hRGuIv2YvGpEOtUmDe41W9kghqEdUlZcMQz"
    geolocator = Bing(BingAPIkey)

    cache = Cache('test.db')
    locationString = '1 Murphy St, Sunnyvale, CA'
    geoBLOB = cache.location_cached(locationString)
    if geoBLOB:
        print('was cached: {}\n{}'.format(geoBLOB, pprint.pformat(geoBLOB.raw)))
    else:
        print('was not cached, looking up and caching now')
        geoBLOB = geolocator.geocode(locationString)
        print('found as: {}\n{}'.format(geoBLOB, pprint.pformat(geoBLOB.raw)))
        cache.save_to_cache(locationString, geoBLOB)
        print('... and now cached.')
        
