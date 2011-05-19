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
    for keyword in keywordList:
        wrapNYTimes(keyword[0], 1)
        wrapWPost(keyword[0], 1)
    maestro.analyzeAll()