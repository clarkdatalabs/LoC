'''
Created on Dec 5, 2017
This module cycles through all of the parts of LOC book metadata and builds the LoC.db SQLite database
availabe at https://web.archive.org/web/20170528203707/http://www.loc.gov/cds/products/MDSConnect-books_all.html
@author: DJT
'''
# import tempfile #used for handling temporary downloads of LOC catalog parts
import gzip
import shutil
from XML_to_SQL import XML2DB

# tmpfile = tempfile.TemporaryFile()

written = 0
scanned = 0

#assumes all book parts are compressed and in subfolder BooksXML/
for part in range(1, 42):
    filePath = 'BooksXML/BooksAll.2014.part' + str(part).zfill(2) + '.xml.gz'
    with open('tmpfile', "wb") as tmp:
        shutil.copyfileobj(gzip.open(filePath), tmp)
    X = XML2DB('tmpfile', 'LoC.db')
    written += X.get("write")
    scanned += X.get("scan")
    print("Part", part, "scan complete.")
    print("Cumulative", written, "records written out of", scanned, "scanned")

    # print(tmp)