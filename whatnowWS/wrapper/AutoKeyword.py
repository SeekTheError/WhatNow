from urllib import urlopen
from xml.dom.minidom import *

keywordList = []

def NYTMostSearched():
    global keywordList
    url = 'http://www.nytimes.com/gst/mostpopular.html'
    try:
        text = urlopen(url).read()
    except:
        print 'error occur during connect to url %s and read contents' % url
        return
    index = text.find('<p class="summary">Keywords most frequently searched by NYTimes.com readers.</p>')
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
            print keyword
        text = text[end:]


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
            print keyword
        text = text[end:]
    

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
            print keyword
        text = text[end:]


def checkDuplication(keyword):
    global keywordList
    for i in keywordList:
        if keyword.upper()==i[0].upper():
            return True
    return False


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
        text = text[text.find('>',index)+1:text.find('</b>',index)]
        pop = int(text)
        keyword[1]=pop
        print keyword[0], pop


def toXML():
    global keywordList
    impl = getDOMImplementation()
    doc = impl.createDocument(None, 'tags', None)
    root = doc.documentElement
    keywordList.sort(cmp)
    for keyword in keywordList[:15]:
        node = doc.createElement('a')
        node.setAttributeNS(None, 'href', '#')
        node.setAttributeNS(None, 'style', 'font-size: 20pt;')
        node.setAttributeNS(None, 'color', '0xccff00')
        node.setAttributeNS(None, 'hicolor', '0x123456')
        keyword = doc.createTextNode(keyword[0])
        node.appendChild(keyword)
        root.appendChild(node)
    print doc.toprettyxml()
    doc.writexml(file('cloud_data.xml', 'w'))


def cmp(e1, e2):
    if (e1[1]>e2[1]):
        return -1
    elif (e1[1]==e2[1]):
        return 0
    else:
        return 1


def wrapKeyword():
    global keywordList
    NYTMostPopular()
    NYTMostSearched()
    WPTopics()
    measurePop()
    toXML()
    print keywordList
    return keywordList


#################TEST####################
if __name__ == '__main__':
    wrapKeyword()
