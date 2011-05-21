import sys
sys.path.insert(0, '..')
from NYTimes import wrapNYTimes
from WashingtonPost import wrapWPost
from AutoKeyword import wrapKeyword
from processing import maestro
from couchdbinterface import dblayer
from couchdbinterface.entities import *

"""
This file is made only for testing
"""
if __name__ == '__main__':
    view=dblayer.view("article/test")
    for u in view :
        a = Article(u.id)
        a=a.findById()
        #a.isAnalyzed = False
        #a.update()
        getDb().delete(a)
    keywordList = wrapKeyword()
    for i in range(10):
        if(i<len(keywordList)):
            keyword = keywordList[i]
        else:
            break
        #keyword, maxPage, past day
        wrapNYTimes(keyword[0], 1, 1)
        wrapWPost(keyword[0], 1, 1)
    maestro.analyzeAll()