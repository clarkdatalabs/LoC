"""
This routine counts the number of records in all of the XML book parts
"""

import gzip
import shutil
from lxml import etree


#42
nodeCount = 0
recordCount = 0

for part in range(41, 42):
    #filePath = '../BooksXML/BooksAll.2014.part02.xml/BooksAll.part02_ZZZ.xml'
    filePath = '../BooksXML/BooksAll.2014.part' + str(part).zfill(2) + '.xml.gz'
    with open('tmpfile', "wb") as tmp:
        shutil.copyfileobj(gzip.open(filePath), tmp)

    #     # XML is too big to load to memory. Set up a iterative context for reading XML on the fly
        context = etree.iterparse('tmpfile', events=('start', 'end'), huge_tree=True, recover=True)
        context = iter(context)
        # save root element so it can be cleared on every iteration (otherwise memory error)
        event, root = next(context)

        nodeCountTemp = 0
        recordCountTemp = 0
        for event, elem in context:
            try:
                if event =='start' and etree.QName(elem.tag).localname == 'record':
                    recordCountTemp += 1
            # catch any oddities in XML parsing with an exception
            except Exception as ex:
                print(ex)

            elem.clear()
            root.clear()
            nodeCountTemp += 1

    print(recordCountTemp, "records and", nodeCountTemp, "nodes read in" "In file", filePath)
    print("cumulative:", nodeCount, "nodes", recordCount, "records")
