from urllib import urlopen
from xml.dom.minidom import *

def NYTMostSearched():
    keywordList = []
    url = 'http://www.nytimes.com/gst/mostpopular.html'
    text = urlopen(url).read()
    index = text.find('<p class="summary">Keywords most frequently searched by NYTimes.com readers.</p>')
    text = text[index:text.find('</ol>',index)]
    while 1:
        i = text.find('href')
        if i==-1:
            break
        text = text[i:]
        start = text.find('>')+1
        end = text.find('<')
        keywordList.append(text[start:end])
        text = text[end:]
    return keywordList


def NYTMostPopular():
    keywordList = []
    url = 'http://topics.nytimes.com/topics/reference/timestopics/index.html'
    text = urlopen(url).read()
    index = text.find('<h3>Most Popular Topics</h3>')
    text = text[index:text.find('</ol>',index)]
    while 1:
        i = text.find('href')
        if i==-1:
            break
        text = text[i:]
        start = text.find('>')+1
        end = text.find('<')
        keywordList.append(text[start:end])
        text = text[end:]
    return keywordList
    

def WPTopics():
    keywordList = []
    url = 'http://www.washingtonpost.com/'
    text = urlopen(url).read()
    index = text.find('<span class="label">In the News</span>')
    text = text[index:text.find('</ul>',index)]
    while 1:
        i = text.find('href')
        if i==-1:
            break
        text = text[i:]
        start = text.find('>')+1
        end = text.find('<')
        keywordList.append(text[start:end])
        text = text[end:]
    return keywordList


def toXML(keywordList):
    impl = getDOMImplementation()
    doc = impl.createDocument(None, 'tags', None)
    root = doc.documentElement
    for i in keywordList:
        node = doc.createElement('a')
        node.setAttributeNS(None, 'href', '#')
        node.setAttributeNS(None, 'style', 'font-size: 20pt;')
        node.setAttributeNS(None, 'color', '0xccff00')
        node.setAttributeNS(None, 'hicolor', '0x123456')
        keyword = doc.createTextNode(i)
        node.appendChild(keyword)
        root.appendChild(node)
    print doc.toprettyxml()
    doc.writexml(file('cloud_data.xml', 'w'))


def wrapKeyword():
    keywordList = []
    keywordList.extend(NYTMostPopular())
    keywordList.extend(NYTMostSearched())
    keywordList.extend(WPTopics())
    print keywordList
    toXML(keywordList)

#################TEST####################
if __name__ == '__main__':
    wrapKeyword()


