"""
algorithm
retrieve an article
load a python script to do the task

how
10 in parallel
a list of in progress
once on of it is done, load a new process
"""
import sys
sys.path.insert(0, '..')

from couchdbinterface.entities import Article
import analyzeArticle

def createTestArticle() :
  a=Article()
  a._id="http://www.koreaherald.com/lifestyle/Detail.jsp?newsMLId=20110503000756"
  a.source='kh'
  a.title="TEST"
  a.create()
  return a
  
  
if __name__ == '__main__':
  createTestArticle()
  analyzeArticle.perform('http://www.koreaherald.com/lifestyle/Detail.jsp?newsMLId=20110503000756')