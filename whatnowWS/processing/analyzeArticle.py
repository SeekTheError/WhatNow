"""
Algorithm

1 download the article
2 extract the content
3 tf idf of the content
4 remove english words
5 calcul article popularity score on google

"""
import sys
sys.path.insert(0, '..')

from urllib2 import urlopen
from couchdb import Document
from couchdbinterface.entities import *
from couchdbinterface import dblayer
import urllib2
import tfIdf



def perform(articleUrl) :
  #retrieve the article
  print articleUrl
  a=Article(id=articleUrl)
  a=a.findById()
  
  print a.source
  #download of the article
  rawContent = urllib2.urlopen(articleUrl).read()  
  content=extractContent(rawContent,a.source)
  a.content=content
  a.update()
  print a.content
  #tf/idf the results
  words=tfIdf.perform(a.content)
  i=0
  a.tags=[]
  #keep only the 10 first tags
  while i < 9 :
    a.tags.append(words[i].decode('utf8'))
    i+=1
  print a.tags
  a.isAnalyzed=True
  a.update()
  print a
    
  
  
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
  
def extractContent(rawHtml,source):
  soup = BeautifulSoup(rawHtml.decode('utf8'))
  if source == 'kh':
    return extractContentKoreanHerald(soup)
  
  
def extractContentKoreanHerald(soup):
  print 'extracting content: Korea Herald'
  article = soup('div', {'id': '_article'})
  articletext = article[0].text
  cleanarticle = BeautifulStoneSoup(articletext, convertEntities = BeautifulStoneSoup.ALL_ENTITIES).text
  return cleanarticle
   


