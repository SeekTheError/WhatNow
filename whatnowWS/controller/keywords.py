from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from security.userauth import checkSession
from wrapper import AutoKeyword

def get(request):
    AutoKeyword.wrapKeyword()
    return HttpResponse()