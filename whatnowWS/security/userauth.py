from couchdbinterface.entities import User

COOKIE_KEY='kuestions_user'


def checkSession (request,context={}) :
  '''
  add some information to the context for the main page, like user infor, current question, etc
  Only if the user is correctly logged in, otherwise , somme basic info will be add
  like top questions, etc
  '''
  
  cookieValue=None
  if request.COOKIES.__contains__(COOKIE_KEY) : 
    cookieValue= request.COOKIES[COOKIE_KEY]
  if cookieValue :
    user=User(sessionId=cookieValue)
    user=user.findBySessionId()
    if user and checkSessionIsNotExpired(user) :
      context['sessionIsOpen']=True
      context['user']=getUserInfoWrapper(user)
    else :
      context['sessionIsOpen']=False
      context['user']=None
  else : 
    print 'security: no cookie found'
    context['sessionIsOpen']=False
  return context

#TODO, return the real user information  
def getCurrentUser(context) :
  if context['sessionIsOpen'] :
    return context['user']
    

#TODO code this to verify the session didn't expire
def checkSessionIsNotExpired(user) :
  return True
  

def getUserInfoWrapper (user) :
  '''
  This function return a Wrapper from a user contain
  '''
  uiw=User()
  uiw.id=user.id
  uiw.login=user.login
  uiw.resume=user.resume
  return uiw



