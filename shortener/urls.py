from django.conf.urls import patterns, url
from shortener import views

'''
Created on 07/09/2014

@author: jamerson
'''
urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^shorten/$', views.shorten, name='shorten'),
    url('^logout/$',views.logout, name='logout'),
    url(r'^login/$', views.make_login, name='make_login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^make_register/$', views.make_register, name='make_register'),
    url(r'^(?P<actual_identifier>[a-z|0-9]{10})/$', views.redirect, name='redirect'),
    )