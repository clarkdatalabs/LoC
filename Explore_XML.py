

from lxml import etree
from xml.etree.ElementTree import register_namespace


source = "BooksAll.part01.xml"
context = etree.iterparse(source, events=('start', 'end'))
context = iter(context)

event, root = next(context)     #save root element so it can be cleared on every iteration

count = 0
fieldCount = 0
errorCount = 0

#MARC Fields:
# 651 = Subject Added Entry - Geographic Name

MARCfield = "260"

for event, elem in context:
    if event =='start' and etree.QName(elem.tag).localname == 'record':     #etree.QName().localname strips the name space
        for child in elem:
            if etree.QName(child.tag).localname == "datafield":
                if child.get('tag',0) == MARCfield:
                    for subfield in child:
                        try:
                            print(subfield.get("code", "n/a"),subfield.text)
                        except UnicodeEncodeError:
                            print("<<ENCODING ERROR>>")
                            errorCount += 1
                        #print("a")
                    print("---")
                    fieldCount += 1
        count += 1
    elem.clear()
    root.clear()
    if fieldCount==100: break
    if count == 1000000:
        print("1 million records searched without finding 100 populated fields")
        break

print(fieldCount, "MARC field", MARCfield,"s populated in", count, "records (", round(100*fieldCount/count,2), "% ) with", errorCount, "encoding errors")
    

# for event, elem in context:
#     print(event)
#     print(elem.tag)
    
#     print("HEREEADASDA")
#     
#     if event == 'start':
#         count += 1
#         print(count)
#         for child in elem:
#             print(child.tag)
#         elem.clear()
#         
#     if count >=3:
#         break

    
        
        
