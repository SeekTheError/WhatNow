#Author: RemiBouchar
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import  render_to_response
from couchdbinterface.entities import User
import userauth
import uuid


def signin(request) :
  login=request.POST['login']
  password=request.POST['password']
  user=User(login=login)
  user=user.findByLogin()
  password=encode(password)
  if login=='' or password=='' :
    message='Please enter a login and a password'
  elif not user :
    message = 'This account does not exist'
  elif not user.isActivated :
    message= 'This account has not been activated yet'
  elif not user.password == password :
    message= 'wrong login/password combination'
  else : #every thing went fine, the session can be open
    return openSession(request,user)
  #return a response in case an error occurred
  return render_to_response('index.html', {'message': message},context_instance=RequestContext(request))
    
def signout(request) :
  sessionId=None
  if request.COOKIES.__contains__(userauth.COOKIE_KEY) :
    sessionId=request.COOKIES[userauth.COOKIE_KEY]
    user=User(sessionId=sessionId)
    user=user.findBySessionId()
    user.sessionId='XXX'+str(uuid.uuid1())
    user.update()
  response=HttpResponseRedirect('/')
  response.delete_cookie(userauth.COOKIE_KEY)
  return response
  
  
from datetime import datetime
from couchdb.mapping import DateTimeField
from util.encode import encode


def openSession(request,user) :
  print 'trying to open session for ',user.login
  t = loader.get_template('index.html')
  sessionExpire = getTomorowDatetime()
  #print sessionExpire
  field=DateTimeField()
  #field._to_
  #user.sessionExpire=sessionExpire
  user.sessionId= encode(user.login+user.email+str(sessionExpire)+str(uuid.uuid1()))
  user.update()

  #Todo add an expiration date!
  response= HttpResponseRedirect("/");
  response.set_cookie(userauth.COOKIE_KEY, user.sessionId)
  return response
  
from datetime import datetime,timedelta
def getTomorowDatetime() :
  oneDay=timedelta(hours=24)
  now=datetime.now()
  return now+oneDay
  


  
