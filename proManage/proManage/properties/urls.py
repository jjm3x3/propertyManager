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
from proManage.properties import views
from .views import *

urlpatterns = patterns('',
     url(r'^$', 'django.contrib.auth.views.login',{'template_name': 'properties/login.html'} , name='login'),
     url(r'^landing$', views.landing, name='landing'),
     url(r'^user_list$', views.user_list, name='user_list'),
     url(r'^property_list$', views.property_list, name='property_list'),
     url(r'^report_list$', views.report_list, name='report_list'),
     url(r'^report_new$', views.report_create, name='report_new'),
     url(r'^report_delete/(?P<pk>\d+)$', views.report_delete, name='report_delete'),
     url(r'^report_delete/(?P<pk>)$', views.report_no_delete, name='report_delete'),
     url(r'^new$', views.user_create, name='user_new'),
     url(r'^property_new$', views.property_create, name='property_new'),
     url(r'^add_manager/(?P<pk>\d+)$', views.add_manager, name='add_manager'),
     url(r'^add_tenant/(?P<pk>\d+)$', views.add_tenant, name='add_tenant'),
     url(r'^unit_add/(?P<pk>\d+)$', views.unit_create, name='unit_add'),
     url(r'^edit/(?P<pk>\d+)$', views.user_update, name='user_edit'),
     url(r'^logout$', views.logout_view, name='logout'),
     url(r'^sorry$', views.sorry, name='sorry'),
     url(r'^property_edit/(?P<pk>\d+)$', views.property_update, name='property_edit'),
     url(r'^remove_manager/(?P<pk>\d+)/(?P<mgr>\d+)$', views.remove_manager, name='remove_manager'),
     url(r'^remove_tenant/(?P<pk>\d+)/(?P<ten>\d+)$', views.remove_tenant, name='remove_tenant'),
     url(r'^unit_edit/(?P<pk>\d+)$', views.unit_update, name='unit_edit'),
     url(r'^delete/(?P<pk>\d+)$', views.user_delete, name='user_delete'),
     url(r'^delete/(?P<pk>)$', views.no_delete, name='user_delete'),
     url(r'^property_delete/(?P<pk>\d+)$', views.property_delete, name='property_delete'),
     url(r'^property_delete/(?P<pk>\d+)$', views.property_no_delete, name='property_delete'),
     url(r'^unit_delete/(?P<pk>\d+)$', views.unit_delete, name='unit_delete'),
     url(r'^unit_delete/(?P<pk>\d+)$', views.unit_no_delete, name='unit_delete'),
     url(r'^unit_view_info/(?P<pk>\d+)$', views.unit_view_info, name='unit_view_info'),
     url(r'^workorder_list$', views.workorder_list, name='workorder_list'),
     url(r'^workorder_new$', views.workorder_create, name='workorder_new'),
     url(r'^workorder_edit/(?P<pk>\d+)$', views.workorder_update, name='workorder_edit'),
)


