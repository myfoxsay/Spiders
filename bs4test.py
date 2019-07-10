from bs4 import BeautifulSoup
soup=BeautifulSoup('<p>Hello</p>','lxml')
print(soup.p.string)

from pyquery import PyQuery as pq
doc=pq('<p>Hello</p>')
print(doc('p').append(" world").text())



