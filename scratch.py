import re

def cleanDate(d, dateKey = '260c'):
    '''finds the input dateKey in the dictionary d. The value is expected to be a list of strings.
    strips the first 4 digits from the first string in this list, and replaces the list with these digits.
    If fewer than 4 consecutive numbers are found, this element is removed from the dictionary'''
    try:
        d[dateKey] = int(re.findall('\d\d\d\d+', d[dateKey][0])[0])
    except:
        if dateKey in d.keys(): 
            d.pop(dateKey) 
            
d = {'260c':['sd2111as3234a','3333','4444a']}
dateKey = '260c'

print('dictionary:',d)
print('entry',d[dateKey])
print('findall',re.findall(r'(?<!\d)\d{4}(?!\d)', d[dateKey][0]))
print('int',int(re.findall('\d\d\d\d', d[dateKey][0])[0][0:4]))

print(cleanDate(d))