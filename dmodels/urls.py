from django.conf.urls import patterns, url

from dmodels import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
 	url(r'^ajax_get_list/(?P<model_name>\w+)/$', views.ajax_get_list, name='ajax_get_list'),	
# 	url(r'^ajax_get_list/(?P<model_name>\w+)$', views.ajax_get_list),	
 	url(r'^ajax_add/(?P<model_name>\w+)/$', views.ajax_add, name='ajax_add'),	
 	url(r'^ajax_change/(?P<model_name>\w+)/(?P<row_id>\d+)/$', views.ajax_change, name='ajax_change' ),	 	
# 	url(r'^(?P<model_name>\w+)/$', views.detail, name='detail'),	
)