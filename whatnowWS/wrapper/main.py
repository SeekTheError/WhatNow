import sys
sys.path.insert(0, '..')
from NYTimes import wrapNYTimes
from WashingtonPost import wrapWPost
from AutoKeyword import wrapKeyword
from processing import maestro
from couchdbinterface import dblayer
from couchdbinterface.entities import *

"""
First delete all existing articles.
Wrapping keywords from topics.nytimes.com
Gathering articles from nyt and wp.
"""
if __name__ == '__main__':
    view=dblayer.view("article/test")
    for u in view :
        a = Article(u.id)
        a=a.findById()
        getDb().delete(a)
    keywordList = wrapKeyword()
    for i in range(1):
        if(i<len(keywordList)):
            keyword = keywordList[i]
        else:
            break
        #keyword, maxPage, past day
        wrapNYTimes(keyword[0], 1, 3)
        wrapWPost(keyword[0], 1, 3)
    maestro.analyzeAll()