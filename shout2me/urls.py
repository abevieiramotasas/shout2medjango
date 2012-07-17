from django.conf.urls import patterns, include, url
from tastypie.api import Api
from rest.api.resources import (UserResource, MessageResource, IslandResource)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

u_api = Api(api_name="rest")
u_api.register(UserResource())
u_api.register(IslandResource())
u_api.register(MessageResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'shout2me.views.home', name='home'),
    # url(r'^shout2me/', include('shout2me.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(u_api.urls)),
)
