import sys
sys.path.insert(0, '..')
from HTMLParser import HTMLParser
from urllib import urlopen
from couchdb import Server
from couchdb.mapping import Document, TextField, IntegerField, DateField
from couchdbinterface import entities

class WPostParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.queue = []
        self.isResult = False
        self.isTitle = False
        self.isDate = False
        self.isSumm = False
        self.numDiv = 0
        
    def handle_starttag(self, tag, attrs):
        if (self.isResult):
            if (tag == 'div'):
                self.numDiv += 1
            elif (tag == 'p' and attrs):
                if (attrs[0][0] == 'class' and attrs[0][1] == 'kicker'):
                    self.isDate = True
                    self.queue.append('<date>')
                elif (attrs[0][0] == 'class' and attrs[0][1] == 'teaser'):
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
                if (self.isDate):
                    self.isDate = False
                    self.queue.append('</date>')
                elif (self.isSumm):
                    self.isSumm = False
                    self.queue.append('</summ>')
            elif (tag == 'h2' and self.isTitle):
                self.isTitle = False
                self.queue.append('</title>')
            
    def handle_data(self, data):
        if(self.isDate or self.isSumm or self.isTitle):
            self.queue.append(data)
    
    def handle_charref(self, name):
        if (self.isTitle or self.isSumm):
            self.queue.append('&#'+name+';')
            
    def storeArticle(self, keyword):
        while(len(self.queue) != 0):
            article = self.parseArticle()
            if (article == None):
                continue
            article.source = 'wp'
            article.create()
            
    def parseArticle(self):
        title = ''
        date = ''
        url = ''
        summ = ''
        while (True):
            elem = self.queue.pop(0)
            if (elem == '<article>'):
                continue
            elif (elem == '<date>'):
                date = self.parseDate()
            elif (elem == '<title>'):
                (title, url) = self.parseTitle()
            elif (elem == '<summ>'):
                summ = self.parseSumm()
            elif (elem == '</article>'):
                break
        if (date == ''):
            return None
        else:
            article = entities.Article()
            article.title = title
            article.date = date
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
        #print 'date: ' +date
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
        #print 'title: '+title
        #print 'url: '+url
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
        #print 'summ: '+summ
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

def wrapWPost(keyword, maxPage = 10, pastDay = 60):
    for i in range(maxPage):
        print 'wrapping WPost : page '+str(i+1)
        wp = WPostParser()
        url = 'http://www.washingtonpost.com/newssearch/search.html?st=%s&cp=%d&scoa=Past+%d+days' % (keyword, i+1, pastDay)
        wp.feed(urlopen(url).read())
        wp.storeArticle(keyword)
        wp.close()
    print 'done'

#################TEST####################
if __name__ == '__main__':
    keyword = 'bin laden'
    wrapWPost (keyword)