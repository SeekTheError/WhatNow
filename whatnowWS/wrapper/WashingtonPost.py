import sys
sys.path.insert(0, '..')
from HTMLParser import HTMLParser
from urllib import urlopen
from couchdb import Server
from couchdb.mapping import Document, TextField, IntegerField, DateField, date
from couchdbinterface.entities import *
from couchdbinterface import dblayer
from datetime import timedelta

class WPostParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.queue = []
        self.isResult = False
        self.isTitle = False
        self.isSumm = False
        self.numDiv = 0
        
    def handle_starttag(self, tag, attrs):
        if (self.isResult):
            if (tag == 'div'):
                self.numDiv += 1
            elif (tag == 'p' and attrs):
                if (attrs[0][0] == 'class' and attrs[0][1] == 'teaser'):
                    self.isSumm = True
                    self.queue.append('<summ>')
            elif (tag == 'h2'):
                self.isTitle = True
                self.queue.append('<title>')
            elif (tag == 'a' and attrs and self.isTitle):
                if (attrs[0][0] == 'href'):
                    self.queue.append('<url>')
                    self.queue.append(attrs[0][1])
        elif (tag == 'div' and attrs):
            if(attrs[0][0] == 'class' and attrs[0][1] == 'resultBlock'):
                self.isResult = True
                self.queue.append('<article>')
                
    def handle_endtag(self, tag):
        if (self.isResult):
            if (tag == 'div'):
                if (self.numDiv == 0):
                    self.isResult = False
                    self.queue.append('</article>')
                else:
                    self.numDiv -= 1
            elif (tag == 'p'):
                if (self.isSumm):
                    self.isSumm = False
                    self.queue.append('</summ>')
            elif (tag == 'h2' and self.isTitle):
                self.isTitle = False
                self.queue.append('</title>')
            
    def handle_data(self, data):
        if(self.isSumm or self.isTitle):
            self.queue.append(data)
    
    def handle_charref(self, name):
        if (self.isTitle or self.isSumm):
            self.queue.append('&#'+name+';')
            
    def storeArticle(self, keyword, searchDate):
        while(len(self.queue) != 0):
            article = self.parseArticle()
            if (article == None):
                continue
            article.date = searchDate
            article.keyword = keyword
            article.source = 'wp'
            print article._id
            print article.title
            print article.extract
            print article.date
            article.create()
            
    def parseArticle(self):
        title = ''
        url = ''
        summ = ''
        while (True):
            elem = self.queue.pop(0)
            if (elem == '<article>'):
                continue
            elif (elem == '<title>'):
                (title, url) = self.parseTitle()
            elif (elem == '<summ>'):
                summ = self.parseSumm()
            elif (elem == '</article>'):
                break
        if url=='':
            return None
        else:
            article = Article()
            article.title = title
            article._id = url
            article.link = url
            article.extract = summ
            return article
        
    def parseDate(self):
        date = ''
        while (True):
            elem = self.queue.pop(0)
            if (elem == '</date>'):
                break
            else:
                date += elem
        date = date[date.find('|')+1:]
        date = self.deleteSpace(date) 
        return DateField()._to_python(date)

    def parseTitle(self):
        title = ''
        url = ''
        while (True):
            elem = self.queue.pop(0)
            if (elem == '<url>'):
                url = self.queue.pop(0)
            elif (elem == '</title>'):
                break
            else:
                title += elem
        title = self.deleteSpace(title)
        return (title, url)
    
    def parseSumm(self):
        summ = ''
        while (True):
            elem = self.queue.pop(0)
            if (elem == '</summ>'):
                break
            else:
                summ += elem
        summ.strip()
        return summ
    
    def deleteSpace(self, string):
        index = string.find('\r')
        while (index != -1):
            string = string[:index] + string[index+1:]
            index = string.find('\r')
        index = string.find('\n')
        while (index != -1):
            string = string[:index] + string[index+1:]
            index = string.find('\n')
        index = string.find('\t')
        while (index != -1):
            string = string[:index] + string[index+1:]
            index = string.find('\t')
        if (len(string)<=0):
            return string
        while (True):
            if (string[0] == ' '):
                string = string[1:]
            else:
                break
        while (True):
            if (string[-1] == ' '):
                string = string[:-1]
            else:
                break
        return string

def wrapWPost(keyword, maxPage = 1, pastDay = 7):
    searchDate = date.today()
    oneDay = timedelta(days=1)
    for i in range(pastDay):
        y = str(searchDate.year)
        m = str(searchDate.month)
        d = str(searchDate.day)
        if (len(m)==1):
            m = '0'+m
        if (len(d)==1):
            d = '0'+d
        sd = y+m+d
        for j in range(maxPage):
            wp = WPostParser()
            url = 'http://www.washingtonpost.com/newssearch/search.html?sa=as&sd=%s&ed=%s&st=%s&cp=%d' % (sd, sd, keyword, j+1)
            url += '&fa_1_sourcenavigator=%22The+Washington+Post%22&fa_1_sourcenavigator=washingtonpost.com&fa_1_mediatypenavigator=^Articles%24'
            try:
                text = urlopen(url).read()
            except:
                print 'error occur during connect to url %s and read contents' % url
                continue
            try:
                wp.feed(text.decode('cp949', errors='replace'))
            except:
                print 'error occur during parsing %s' % url
                continue
            print 'wrapping WashingtonPost : '+str(searchDate)+', page '+str(j+1)
            print url
            wp.storeArticle(keyword, searchDate)
            wp.close()
        searchDate -= oneDay
    print 'done'

#################TEST####################
if __name__ == '__main__':
    view=dblayer.view("article/test")
    for u in view :
        a = Article(u.id)
        a=a.findById()
        getDb().delete(a)
    keyword = 'laden'
    wrapWPost (keyword, 1, 3)