

from lxml import etree
from xml.etree.ElementTree import register_namespace
import sqlite3
from _collections import defaultdict
import os

#clear previous versions of the database
db = 'LoC.db'
#os.remove(db)

conn = sqlite3.connect(db)
c = conn.cursor()

x = c.execute('''SELECT MAX(recordID) FROM Record''').fetchone()[0]

#initialize tables
c.execute('''CREATE TABLE IF NOT EXISTS Record (
                recordID integer PRIMARY KEY,
                callNumber text,
                pubLocation text,
                pubDate text
                )'''
          )
c.execute('''CREATE TABLE IF NOT EXISTS Location (
                recordID integer,
                subjectLocation text,
                FOREIGN KEY (recordID) REFERENCES Record(recordID)
                )'''
          )
recordID = 1


source = "BooksAll.part01.xml"
context = etree.iterparse(source, events=('start', 'end'))
context = iter(context)

event, root = next(context)     #save root element so it can be cleared on every iteration

#MARC Fields:
# 050 a = Library of Congress Call Number
# 260 a = Publication Location
# 260 c = Publication Date
# 650 a = Subject Added Entry - Geographic Name

MARCfields = {"050": ['a'], "260": ['a','c'], "651": ['a']}

recordCount = 1

fields = sum(len(MARCfields[key]) for key in MARCfields.keys()) #count number of fields listed for validation later
for event, elem in context:
    if event =='start' and etree.QName(elem.tag).localname == 'record':     #etree.QName().localname strips the name space
        d = defaultdict(list)   #set so we can use append() to create new dictionary list values
        for child in elem:
            if etree.QName(child.tag).localname == "datafield":
                tag = child.get('tag',0)                
                if tag in MARCfields.keys():
                    for subfield in child:
                        code = subfield.get("code",0) 
                        if code in MARCfields[tag]:
                            d[(tag+code)].append(subfield.text)
        #print(d)
        
        #if all fields are populated for a given record, add it to the database
        if len(d) == fields:
            recordID += 1
            #insert row into 'Record' table
            t = (recordID,
                 d['050a'][0],
                 d['260a'][0],
                 d['260c'][0])
            c.execute("INSERT INTO Record VALUES (?,?,?,?)", t)
            for location in d['651a']:
                t = (recordID, location)
                c.execute("INSERT INTO Location VALUES (?,?)", t)
            del(t)
#        else:
#            print("FIELDS MISSING, THROW AWAY RECORD")
#        print("---")
        del(d)
    elem.clear()
    root.clear()
    recordCount += 1
    #if recordID >= 1000: break
    
conn.commit()
conn.close()



print(recordID, "records written out of", recordCount, "scanned (", round(((recordID/recordCount)*100),2), "%)")