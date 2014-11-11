from django.conf.urls import patterns, include, url
from django.contrib import admin
import sami

urlpatterns = patterns('',

    url(r'^', include('sami.urls')), #sami irls
    url(r'^admin/', include(admin.site.urls)),
)
