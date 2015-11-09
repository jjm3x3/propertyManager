"""proManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
    url(r'^properties/$', PropertyList.as_view(), name='propertylisting'),
    url(r'^units/$', UnitList.as_view(), name='unitlisting'),
    url(r'^tenantinfo/$', TenantInfoList.as_view(), name="tenantinfolisting"),
    url(r'^unitgroups/$', UnitGroupList.as_view(), name="unitgrouplisting"),
    url(r'^createproperty/$', PropertyCreate.as_view(), name='propertycreate'),
    url(r'^(?P<pk>\d+)/$', PropertyDetail.as_view(), name='propertydetail'),
    url(r'^(?P<pk>\d+)/update/$', PropertyUpdate.as_view(), name='propertyupdate'),
    url(r'^(?P<pk>\d+)/delete/$', PropertyDelete.as_view(), name='propertydelete')
)


