

from lxml import etree
from xml.etree.ElementTree import register_namespace
import sqlite3
from _collections import defaultdict
import os
import re



def cleanDate(d, dateKey = '260c'):
    '''Finds the input dateKey in the dictionary d. The value is expected to be a list of strings.
    strips the first instance of exactly 4 consecutive digits 4 digits from the first string in this list, 
    and replaces the list with these digits. If there never appear 4 consecutive digits then this element is 
    removed from the dictionary.'''
    try:
        d[dateKey] = int(re.findall(r'(?<!\d)\d{4}(?!\d)', d[dateKey][0])[0])
    except:
        if dateKey in d.keys(): 
            d.pop(dateKey) 



def XML2DB(XML, db):
#    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        
        #initialize tables
        c.execute('''CREATE TABLE IF NOT EXISTS Record (
                        recordID integer PRIMARY KEY,
                        callNumber text,
                        pubLocation text,
                        pubDate integer
                        )'''
                  )
        c.execute('''CREATE TABLE IF NOT EXISTS Subject_Location (
                        recordID integer,
                        subjectLocation text,
                        FOREIGN KEY (recordID) REFERENCES Record(recordID)
                        )'''
          )
        
        #get max recordID to increment from. If no rows exist, start at 1
        maxID = c.execute('''SELECT MAX(recordID) FROM Record''').fetchone()[0]
        if maxID: 
            recordID = maxID
        else: 
            recordID = 1
        
        #XML is too big to load to memory. Set up a iterative context for reading XML on the fly
        context = etree.iterparse(XML, events=('start', 'end'))
        context = iter(context)
        #save root element so it can be cleared on every iteration (otherwise memory error)
        event, root = next(context)

        #MARC Fields:
        # 050 a = Library of Congress Call Number
        # 260 a = Publication Location
        # 260 c = Publication Date
        # 650 a = Subject Added Entry - Geographic Name
        MARCfields = {"050": ['a'], "260": ['a','c'], "651": ['a']}
        #count number of fields listed for validation later
        fields = sum(len(MARCfields[key]) for key in MARCfields.keys()) 
        
        #set counters
        recordCount = 1
        writeCount = 0
        
        for event, elem in context:
            if event =='start' and etree.QName(elem.tag).localname == 'record':     #etree.QName().localname strips the name space
                #Build a dictionary to hold sought field data from each record
                d = defaultdict(list)   #set so we can use append() to create new dictionary list values
                for child in elem:
                    if etree.QName(child.tag).localname == "datafield":
                        tag = child.get('tag',0)                
                        if tag in MARCfields.keys():
                            for subfield in child:
                                code = subfield.get("code",0) 
                                if code in MARCfields[tag]:
                                    d[(tag+code)].append(subfield.text)
                
                #clean year field to first 4 consecutive integers found                    
                cleanDate(d, '260c')

                if len(d) == fields:
                    #insert row into 'Record' table
                    t = (recordID,
                         d['050a'][0],
                         d['260a'][0].translate({ord(c): None for c in '[];:?,.'}),
                         d['260c'])
                    c.execute("INSERT INTO Record VALUES (?,?,?,?)", t)
                    for location in d['651a']:
                        t = (recordID, location)
                        c.execute("INSERT INTO Subject_Location VALUES (?,?)", t)
                    del(t)
                    recordID += 1
                    writeCount += 1
                del(d)
            elem.clear()
            root.clear()
            recordCount += 1        
        
        conn.commit()
        conn.close()
        
        print(writeCount, "records written out of", recordCount, "scanned in document", XML ,"(", round(((recordID/recordCount)*100),2), "%)")
#    except:
#        print("an error occurred")


   
source = "BooksAll.part01.xml"
#source = 'LoC_snippet.xml'
db = 'LoC.db'
os.remove(db)
XML2DB(source, db)
