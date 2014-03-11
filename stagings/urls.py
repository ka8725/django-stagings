from django.conf.urls import patterns, url
from stagings.views import IndexView, StagingDetailView

urlpatterns = patterns('',
  url(r'^$', IndexView.as_view(), name='index'),
  url(r'^(?P<pk>\d+)$', StagingDetailView.as_view(), name='detail'),
)
