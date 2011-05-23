#Author Remi Bouchar
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from security.userauth import checkSession, getCurrentUser

def view(request) :
  t = loader.get_template('index.html')
  context=RequestContext(request)
  context=checkSession(request,context)
  return HttpResponse(t.render(context))
  
def addKeyword(request):
  context=checkSession(request,context)
  user = getCurrentUser(context)
  user = user.findById()
  fav=request.GET['favorite']
  user.topics.append(fav);
  
