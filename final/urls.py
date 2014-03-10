from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
import stagings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', lambda x: redirect(reverse('stagings:index'))),
    url(r'^stagings/', include('stagings.urls', namespace='stagings'))
)
