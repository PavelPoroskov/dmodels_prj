from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dmodels_prj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

# dmodels include (
    url(r'^dmodels/', include('dmodels.urls')),    
# dmodels include )    
    url(r'^admin/', include(admin.site.urls)),
)
