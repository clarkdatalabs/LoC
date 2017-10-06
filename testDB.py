
str = "h3110 23 cat 444.4 rabbit 11 2 dog"
l = [int(s) for s in str.split() if s.isdigit()]

print(l)

import re
from _collections import defaultdict


print(int(re.findall('\d\d\d\d+', str)[0]))

d = defaultdict(list)

d={'a':['1842-1901.'],
   'b':['1999','2000'],
   'c':['1899.']}


for key in d.keys():
    try:
        d[key] = int(re.findall('\d\d\d\d+', d[key][0])[0])
    except:
        d.pop(key)
    
print(d)