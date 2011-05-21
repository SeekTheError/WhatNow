#!/usr/bin/env python

import math
from operator import itemgetter

def freq(word, document):
  return document.split(None).count(word)

def wordCount(document):
  return len(document.split(None))

def numDocsContaining(word,documentList):
  count = 0
  for document in documentList:
    if freq(word,document) > 0:
      count += 1
  return count

def tf(word, document):
  return (freq(word,document) / float(wordCount(document)))

def idf(word, documentList):
  return math.log(len(documentList) / numDocsContaining(word,documentList))

def tfidf(word, document, documentList):
  return (tf(word,document) * idf(word,documentList))

if __name__ == '__main__':
  
  documentList = [] 
  doc=open('sample.txt','r')
  for line in doc.readlines() :
    documentList.append(line.replace('"','').replace('.','').replace(',','').lower())
  perform(documentList)
  
def perform(text) : 
  text=text.encode('utf8', errors='replace')
  documentList = []
  for line in text.split(','):
  
    documentList.append(line.lower().replace('\'',' ').replace('(',' ').replace(')',' '))
  
  words = {}
  documentNumber = 0
  for word in documentList[documentNumber].split(None):
    words[word] = tfidf(word,documentList[documentNumber],documentList)
  
  results=[]
  for item in sorted(words.items(), key=itemgetter(1), reverse=True):
    results.append(item[0])
  return results
