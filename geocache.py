
import geopy
import pickle
import sqlite3

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
        cur = self.conn.cursor()
        cur.execute('SELECT geoBLOB FROM Geocache WHERE locationString=?', (locationString,))
        res = cur.fetchone()
        if res is None: return False
        return pickle.loads(res[0])

    def save_to_cache(self, locationString, geoBLOB):
        cur = self.conn.cursor()
        cur.execute('INSERT INTO Geocache(locationString, geoBLOB) VALUES(?, ?)',
                    (locationString, sqlite3.Binary(pickle.dumps(geoBLOB, -1))))
        self.conn.commit()
  
  
        
if __name__ == '__main__':
    # run a small test in this case
    import pprint
    from geopy.geocoders import Bing
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
        
