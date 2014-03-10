from django.conf.urls import patterns, url
from stagings.views import IndexView

urlpatterns = patterns('',
  url(r'^$', IndexView.as_view(), name='index'),
)
