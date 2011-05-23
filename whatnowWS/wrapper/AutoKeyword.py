from urllib import urlopen
from xml.dom.minidom import *
from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
import json

import sys
sys.path.insert(0, '..')
from couchdbinterface.entities import Keyword

#Sotre keywords = (keyword, popularity)
keywordList = []
maxKeywordNum = 20
SEARCH_BASE ="http://api.twitter.com/1/trends/weekly.json"

def twitterSearch():
    url = SEARCH_BASE + '?' + 'output=json&exclude=hashtags'
    result = json.load(urlopen(url))
    return result['trends']

def search():
  global keywordList
  info = twitterSearch()
  url = 'http://api.twitter.com/1/trends/weekly.json?output=json&exclude=hashtags'
  try:
      text = urlopen(url).read()
  except:
      print 'error occur during connect to url %s' % url
      return
  index1 = text.find('"trends":{"')+11
  index2 = text.find('":[{"',index1)
  text = text[index1:index2]
  for item in info[text]:
      keywordList.append([item['query'],0])

#Gather top 50 most searched keyword from nytimes.
#It may be best choice.
def NYTMostSearched():
    global keywordList
    url = 'http://www.nytimes.com/gst/mostsearched.html?&period=7'
    try:
        text = urlopen(url).read()
    except:
        print 'error occur during connect to url %s and read contents' % url
        return
    soup = BeautifulSoup(text.decode('utf8'))
    result = soup('div', {'class': 'result'})
    for elem in result:
        keyword = elem.text
        keyword = keyword[keyword.find('.')+1:keyword.find('&raquo;')]
        keywordList.append([keyword, 0])
    '''
    for keyword in parser.results:
        if (not checkDuplication(keyword)):
            keywordList.append([keyword, 0])
            print keyword
    '''

#Ggather most popular topics from nytimes.
#Not good, it seems do not change frequently, and topics are old.
def NYTMostPopular():
    global keywordList
    url = 'http://topics.nytimes.com/topics/reference/timestopics/index.html'
    try:
        text = urlopen(url).read()
    except:
        print 'error occur during connect to url %s and read contents' % url
        return
    index = text.find('<h3>Most Popular Topics</h3>')
    text = text[index:text.find('</ol>',index)]
    while 1:
        i = text.find('href')
        if i==-1:
            break
        text = text[i:]
        start = text.find('>')+1
        end = text.find('<')
        keyword = text[start:end].strip()
        if (not checkDuplication(keyword)):
            keywordList.append([keyword, 0])
        text = text[end:]

#Gather keywords which is shown in main page from wp.
#Not good, it changes too frequently, and it looks like gossips.
def WPTopics():
    global keywordList
    url = 'http://www.washingtonpost.com/'
    try:
        text = urlopen(url).read()
    except:
        print 'error occur during connect to url %s and read contents' % url
        return
    index = text.find('<span class="label">In the News</span>')
    text = text[index:text.find('</ul>',index)]
    while 1:
        i = text.find('href')
        if i==-1:
            break
        text = text[i:]
        start = text.find('>')+1
        end = text.find('<')
        keyword = text[start:end].strip()
        if (not checkDuplication(keyword)):
            keywordList.append([keyword, 0])
        text = text[end:]

#Check whether already same keyword exists in the keywordList.
#If gather keywords from only one source, it is not necessary. 
def checkDuplication(keyword):
    global keywordList
    for i in keywordList:
        if keyword.upper()==i[0].upper():
            return True
    return False

#Search keywords at wp and get number of results. 
def measurePop():
    global keywordList
    for keyword in keywordList:
        try:
            url = 'http://www.washingtonpost.com/newssearch/search.html?st=%s' % (keyword[0])
            text = urlopen(url).read()
        except:
            print 'error occur during connect to url %s and read contents' % url
            continue
        index = text.find('<b id="resultsCount">')+1
        if index==0:
            keyword[1]=0
        else:
            text = text[text.find('>',index)+1:text.find('</b>',index)]
            pop = int(text)
            keyword[1]=pop
        print keyword[0], keyword[1]

#Convert keywordList to XML file which is used to display keywords in cloud.
def toXML():
    global keywordList
    impl = getDOMImplementation()
    doc = impl.createDocument(None, 'tags', None)
    root = doc.documentElement
    global maxKeywordNum
    for i in range(maxKeywordNum):
        if(i < len(keywordList)):
            keyword = keywordList[i]
        else:
            break
        node = doc.createElement('a')
        #node.setAttributeNS(None, 'href', '/timeline/?key='+keyword[0])
        node.setAttributeNS(None, 'href', 'javascript:cloudCallback("'+keyword[0]+'");');#'cloudCallback('+keyword[0]+');')
        #node.setAttributeNS(None, 'target', 'content')
        if (i <= 5):
            node.setAttributeNS(None, 'style', 'font-size: 15pt;')
            node.setAttributeNS(None, 'color', '0xff0099')
            node.setAttributeNS(None, 'hicolor', '0x14d3ff')
        elif (i > 5 and i <= 13):
            node.setAttributeNS(None, 'style', 'font-size: 11pt;')
            #node.setAttributeNS(None, 'color', '0xccff00')
            node.setAttributeNS(None, 'hicolor', '0xff1d07')
        else:
            node.setAttributeNS(None, 'style', 'font-size: 7pt;')
            node.setAttributeNS(None, 'color', '0x505050')
            node.setAttributeNS(None, 'hicolor', '0x123456')                                    
        keyword = doc.createTextNode(keyword[0])
        node.appendChild(keyword)
        root.appendChild(node)
    print doc.toprettyxml()
    doc.writexml(file('../static/cloud_data.xml', 'w'))

#Cmp function to sorting keywrodList by popularity
def cmp(e1, e2):
    if (e1[1]>e2[1]):
        return -1
    elif (e1[1]==e2[1]):
        return 0
    else:
        return 1

#store keywords in db
def storeKeyword():
    f = file('../keyword.txt', 'w')
    for u in keywordList:
        f.write(u[0]+'\n')
        keyword = Keyword()
        keyword._id=u[0]
        keyword.popularity=u[1]
        #keyword.create()

#Gather keywords from sources, measure popularity, sort it, convert to XML file and return.
def wrapKeyword():
    global keywordList
    NYTMostSearched()
    search()
    #NYTMostPopular()    not good
    #WPTopics()    not good
    #measurePop()    not good, number of article does not mean popularity of keyword
    toXML()
    storeKeyword()
    print keywordList
    return keywordList


#################TEST####################
if __name__ == '__main__':
    wrapKeyword()
