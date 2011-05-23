import sys
sys.path.insert(0, '..')
from NYTimes import wrapNYTimes
from WashingtonPost import wrapWPost
from AutoKeyword import wrapKeyword
from processing import maestro
from processing import analyzeArticle
from couchdbinterface import dblayer
from couchdbinterface.entities import *

"""
First delete all existing articles.
Wrapping keywords from topics.nytimes.com
Gathering articles from nyt and wp.
"""

def perform():
    keywordList = wrapKeyword()
    for i in range(50):
        if(i<len(keywordList)):
            keyword = keywordList[i]
        else:
            break
        #keyword, maxPage, past day
        print "WRAPPING THE NY TIMES WHIT KEYWORD: "+keyword[0]
        wrapNYTimes(keyword[0])
        print "WRAPPING THE WASHINGTON POST WHIT KEYWORD: "+keyword[0]
        wrapWPost(keyword[0])
   

def wrap():
  f=open('keywords.txt','r')
  for keyword in f.readlines():
    print "WRAPPING THE NY TIMES WHIT KEYWORD: "+keyword.replace('\n','')
    wrapNYTimes(keyword)
    print "WRAPPING THE WASHINGTON POST WHIT KEYWORD: "+keyword.replace('\n','')
    wrapWPost(keyword)

if __name__ == '__main__':
    wrap();
