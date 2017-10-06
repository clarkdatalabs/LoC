from _collections import defaultdict
from lxml import etree
from xml.etree.ElementTree import register_namespace

def parseRecord(elem, MARCfields):
    try:
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
    except:
        print("parseRecord failed")
        
    