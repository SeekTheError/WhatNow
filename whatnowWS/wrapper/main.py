import sys
sys.path.insert(0, '..')
import NYTimes
import WashingtonPost
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
    NYTimes.wrapNYTimes('laden', 10)
    WashingtonPost.wrapWPost('laden', 10)
    maestro.analyzeAll()