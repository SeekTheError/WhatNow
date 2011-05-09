#Author Remi Bouchar
from django.http import HttpResponse,Http404
from urllib2 import *
import couchdbinterface.dblayer as couchVar
from django.shortcuts import render_to_response
from django.utils.encoding import smart_unicode


KUESTIONS_API_GET_URL='/api'

#TODO : modify the url scheme for the api

def searchQuestion(request,parameter) :
  pass


def gate(request) :
  '''
  this method play the role of a security proxy, by only allowing GET method directly to couchdb,
  and then filtering the resulting json to remove some parameter that should remain server side
  '''
  if request.POST :
    keeper(request,'Invalid Acces, use of a POST method')  
  url= '/'+request.path.replace(KUESTIONS_API_GET_URL,couchVar.DB_NAME)
  if request.GET.__contains__('key') :
    param= smart_unicode(request.GET['key'], encoding='utf-8', strings_only=False, errors='strict')
    params='?key='+quote(param.encode('UTF8'))
  if request.GET.__contains__('q') :
    param=smart_unicode(request.GET['q'], encoding='utf-8', strings_only=False, errors='strict')
    params='?q='+quote(param.encode('UTF8'))
    
  import urllib2
  url=unicode(url+params)
  print url
  f=urllib2.urlopen("http://localhost:5984"+url)
  data=''
  for line in f.readlines():
    data+=line
  
  return HttpResponse(removeProtectedFields(data))


def removeProtectedFields(json) : 
  return json
  for field in privateFields :
    json=fieldRe.sub('',json)
  return json



#pre compile the regexp for the removeProtectFields function
#TODO, externalize the field list!
import re
privateFields=['_rev','sessionId','password','session_expire','email','activationCode','isActivated']
expr=''
i=0
for field in privateFields:
  expr+='('+field+')'
  if not i > len(privateFields) - 2 :
    expr+='|'
  i+=1
reString='"('+expr+')":(("[0-9A-Za-z\-@\.]+")|(null)|(true)|(false))'
fieldRe=re.compile(reString)

def keeper(request,message=''):
  print 'WARNING, api: '+message
  return render_to_response('error.html',{'message':'Kuestions API - 403 Forbidden'})
  
  
  
  
        
  
    
    
 
 
  
  
    
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
