from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    # Example:
    (r'^$', 'controller.indexcontroller.view'),
    
    (r'^register/$', 'security.registercontroller.register'),
    (r'^register/(?P<code>\w+)$', 'security.registercontroller.activate'),
    
    (r'^security/signin/$', 'security.securitycontroller.signin'),
    (r'^security/signout/$', 'security.securitycontroller.signout'),
  
     
    
    #For static media files
    (r'^whatnow/media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_MEDIA_ROOT}),
)
