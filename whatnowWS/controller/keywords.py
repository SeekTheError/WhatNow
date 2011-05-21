from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from security.userauth import checkSession
import json


def get(request):
  xml='<a>hello word XML</a>'
  list=['aa','aa','aa']
    
  return HttpResponse(json.dumps(list))
