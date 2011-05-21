import sys
sys.path.insert(0, '..')
from urllib2 import urlopen
from couchdb import Server
from couchdb.mapping import Document, TextField, IntegerField, DateField, date
from couchdbinterface.entities import *
from couchdbinterface import dblayer
from datetime import timedelta
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

#search 'keyword' during 'pastDay' for 'maxPage' which have 'numOfArt' article in 1 page
def wrapNYTimes(keyword, maxPage = 1, pastDay = 7):
    searchDate = date.today()
    oneDay = timedelta(days=1)
    while 1:
        index = keyword.find(' ')
        if index==-1:
            break
        keyword = keyword[:index] + '%20' + keyword[index+1:]
    for i in range(pastDay):
        y = searchDate.year
        m = str(searchDate.month)
        d = str(searchDate.day)
        if (len(m)==1):
            m = '0'+m
        if (len(d)==1):
            d = '0'+d
        url = 'http://query.nytimes.com/search/query?query=%s&daterange=period&year1=%d&mon1=%s&day1=%s&year2=%d&mon2=%s&day2=%s' % (keyword, y, m, d, y, m, d)
        try:
            req = urlopen(url)
            page = req.read()
        except:
            print 'error occur during connect to url %s and read contents' % url
            continue
        soup = BeautifulSoup(page)
        n = resultNum(soup)
        if n>maxPage*10:
            pageNum = maxPage
        else:
            pageNum = (n+9)/10
        for j in range(pageNum):
            url = 'http://query.nytimes.com/search/query?query=%s&daterange=period&year1=%d&mon1=%s&day1=%s&year2=%d&mon2=%s&day2=%s&frow=%d' % (keyword, y, m, d, y, m, d, j*10)
            try:
                req = urlopen(url)
                page = req.read()
            except:
                print 'error occur during connect to url %s and read contents' % url
                continue
            print 'wrapping NYTimes : '+str(searchDate)+', page '+str(j+1)
            print url
            soup = BeautifulSoup(page.decode('utf8', errors='replace'))
            storeArticles(soup, keyword, searchDate)
        searchDate -= oneDay
    print 'done'

#parse result page and store articles in couchdb
def storeArticles(soup, keyword, searchDate):
    result = soup('ol', {'class':'srchSearchResult'})
    if len(result)==1:
        soup2 = BeautifulSoup(result[0].prettify())
    elif len(result)==2:
        soup2 = BeautifulSoup(result[1].prettify())
    else:
        return
    titleList = soup2('h3')
    summaryList = soup2('p', {'class':'summary'})
    urlList = soup2('a')
    for i in range(len(titleList)):
        article = Article()
        article.title=titleList[i].text
        article.date = searchDate
        url = urlList[i].get('href')
        url = url[:url.find('?')]
        article._id = url
        article.link = article._id
        article.extract = summaryList[i].text
        article.keyword = keyword
        article.source = 'nyt'
        print article._id
        print article.title
        print article.extract
        print article.date
        article.create()
    
#return num of search result
def resultNum(soup):
    list = soup('span', {'class':'sortText'})
    if len(list)<=0:
        return 0
    else:
        num = list[-1].text.split()[-2]
        return int(num)

#################TEST####################
if __name__ == '__main__':
    view=dblayer.view("article/test")
    for u in view :
        a = Article(u.id)
        a=a.findById()
        getDb().delete(a)
    wrapNYTimes('laden', 1, pastDay=3)
