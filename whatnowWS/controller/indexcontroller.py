#Author Remi Bouchar
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from security.userauth import checkSession

def view(request) :
  t = loader.get_template('index.html')
  context=RequestContext(request)
  context=checkSession(request,context)
  return HttpResponse(t.render(context))

