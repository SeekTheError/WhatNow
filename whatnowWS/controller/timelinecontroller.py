from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from security.userauth import checkSession

def view(request) :
  t = loader.get_template('timeline.html')
  generateTimeline(request)
  context=RequestContext(request)
  context=checkSession(request,context)
  return HttpResponse(t.render(context))


import datetime
import urllib2
import json
def generateTimeline(request):
  keyword = request.GET['key']
  now=datetime.datetime.now()
  lastWeek=[]
  for i in range (6):
    lastWeek.append(now-datetime.timedelta(days=i));
  baseUrl="http://localhost:5984/whatnowdb/_fti/_design/article/by_title?&q="
  results={}
  
  preJson={}
  preJson['days']=[]
  for day in lastWeek:
    if day.month<10:
      month='0'+str(day.month)
    else :
      month=str(day.month)
    date=str(day.year)+'-'+month+'-'+str(day.day)
    preJson['days'].append(date)
    params=urllib2.quote(keyword)+urllib2.quote(" AND ")+"date:"+date;
    f=urllib2.urlopen(baseUrl+params)
    results[date]=''
    for line in f.readlines():
      results[date]+=line   

  for day in results.iterkeys():
    articles=json.loads(results.get(day))
    if articles.has_key('rows'):
      fields=articles['rows']
      temp=[]
      for field in fields:
        a={'title':field['fields']['title'],'popularity':field['fields']['popularity'],'url':field['id']}
        temp.append(a)
    preJson[day]=temp
    print day
    print preJson[day]
    
    
  return HttpResponse(json.dumps(preJson))   

          
          
        
        
        
        
        
  
