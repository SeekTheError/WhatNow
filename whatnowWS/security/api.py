#Author Remi Bouchar
from django.http import HttpResponse,Http404
import urllib
import couchdbinterface.dblayer as couchVar
from django.shortcuts import render_to_response


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
  url=couchVar.SERVER_URL + request.path.replace(KUESTIONS_API_GET_URL,couchVar.DB_NAME)
  print url
  if request.GET.__contains__('key') :
    param='?key=' + request.GET['key']
    url+=param
  if request.GET.__contains__('q') :
    param='?q=' + request.GET['q']
    url+=param
  f = urllib.urlopen(url)
  if f is not None :
    json=''
    for line in f.readlines() :
      json+=line#.replace('\n','')
    print json
    return HttpResponse(removeProtectedFields(json))
  else :
    keeper(request,'error at the gate')

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

#Define http 5XX instead : internal error, forbiden
def keeper(request,message=''):
  print 'WARNING, api: '+message
  return render_to_response('error.html',{'message':'Kuestions API - 403 Forbidden'})
  
  
  
  
        
  
    
    
 
 
  
  
    
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
