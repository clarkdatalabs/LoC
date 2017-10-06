'''
Created on Sep 15, 2017

@author: DJT
'''

from bs4 import BeautifulSoup
#from io import StringIO

source = "booksexample.xml"

#import xml.etree as ET
from xml.etree.ElementTree import iterparse
infile = open(source,"r")
contents = infile.read()
soup = BeautifulSoup(contents,'xml')
titles = soup.find_all('title')
authors = soup.find_all('author')
for i in range(0, len(titles)):
    print(titles[i].get_text(),"by",authors[i].get_text())
    

##Basic iter example
context = iterparse(source, events=('start', 'end',))
context = iter(context)

#event, root = context.next()

for event, elem in context:
    


for event, elem in context:
    if event == "start" and elem.tag == "book":
        tag = elem.tag
        value = elem.text
        #print(elem)
        for child in elem:
            if child.tag == 'author':
                print(child.text)
    elem.clear()  # clean up


del context



#Iter example 1








##another iter example

# for event, elem in iterparse(source, events=('start', 'end', 'start-ns', 'end-ns')):
#   print(event, elem)
# 
# nsmap = {}
# for event, elem in iterparse(source, events=('start-ns')):
#   ns, author = elem
#   print(elem)
# print(nsmap)


