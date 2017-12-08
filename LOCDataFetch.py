'''
Created on Dec 5, 2017
This module downloads all of the parts Library of Congress book catalog,
availabe at https://web.archive.org/web/20170528203707/http://www.loc.gov/cds/products/MDSConnect-books_all.html
@author: DJT
'''
#import tempfile #used for handling temporary downloads of LOC catalog parts
import gzip
import shutil
from XML_to_SQL import XML2DB

#tmpfile = tempfile.TemporaryFile()

for part in range (2, 3):
    filePath = 'BooksXML/BooksAll.2014.part' + str(part).zfill(2) + '.xml.gz'
    with open('tmpfile', "wb") as tmp:
        shutil.copyfileobj(gzip.open(filePath), tmp)
        XML2DB(tmp, 'test1.db')
        

    #print(tmp)
    

    
    