"""
Algorithm

1 download the article
2 extract the content
3 tf idf of the content
4 remove english words
5 calcul article popularity score on google

"""
"""
use this to add all the module from whatnow to the python path
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
  #sometimes it can't connect to url, so surround with try statement 
  try:
    rawContent = urllib2.urlopen(articleUrl).read()
  except:
    print 'error occur during connect to url %s and read contents' % articleUrl
    return
  content=extractContent(rawContent,a.source)
  a.content=content
  a.update()
  print a.content
  #tf/idf the results
  words=tfIdf.perform(a.content)
  i=0
  a.tags=[]
  #keep only the 10 first tags
  while (i < 10 and i < len(words)) :
    a.tags.append(words[i].decode('utf8', errors='replace'))
    i+=1
  print a.tags
  #measure popularity
  a.popularity=yahooResultNum(articleUrl)
  print a.popularity
  a.isAnalyzed=True
  a.update()
  print a
    
  
  
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
  
def extractContent(rawHtml,source):
  soup = BeautifulSoup(rawHtml.decode('utf8', errors='replace'))
  if source == 'kh':
    return extractContentKoreanHerald(soup)
  if source == 'nyt':
    return extractContentNewYorkTimes(soup)
  if source == 'wp':
    return extractContentWashingtonPost(soup)

  
def extractContentKoreanHerald(soup):
  print 'extracting content: Korea Herald'
  article = soup('div', {'id': '_article'})
  articletext = article[0].text
  cleanarticle = BeautifulStoneSoup(articletext, convertEntities = BeautifulStoneSoup.ALL_ENTITIES).text
  return cleanarticle
      
      
def extractContentNewYorkTimes(soup):
  print 'extracting content: New York Times'
  article = soup('div', {'class': 'articleBody'})
  articletext = ''
  if (len(article) > 0):
      for elem in article:
        articletext += elem.text + ' '
  else:
      article = soup('div', {'class': 'entry-content'})
      for elem in article:
        articletext += elem.text + ' '
  cleanarticle = BeautifulStoneSoup(articletext, convertEntities = BeautifulStoneSoup.ALL_ENTITIES).text
  cleanarticle = cleanarticle.encode('cp949', errors='replace')
  return cleanarticle
  

def extractContentWashingtonPost(soup):
  print 'extracting content: Washington Post'
  article = soup('div', {'class': 'article_body'})
  articletext = ''
  if (len(article) > 0):
      for elem in article:
        articletext += elem.text + ' '
  else:
      article = soup('div', {'id': 'entrytext'})
      for elem in article:
        articletext += elem.text + ' '
  cleanarticle = BeautifulStoneSoup(articletext, convertEntities = BeautifulStoneSoup.ALL_ENTITIES).text
  cleanarticle = cleanarticle.encode('cp949', errors='replace')
  return cleanarticle
  

def yahooResultNum(articleUrl):
    url = 'http://search.yahoo.com/search?p=%s' % '"'+articleUrl+'"'
    try:
        text = urlopen(url).read()
    except:
        print 'error occur during connect to url %s and read contents' % url
        return 0
    index = text.find('<strong id="resultCount">')+1
    num = text[text.find('>', index)+1:text.find('</strong>',index)]
    while 1:
        index=num.find(',')
        if index==-1:
            break
        num=num[:index]+num[index+1:]
    return int(num)


