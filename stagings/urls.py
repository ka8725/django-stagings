from django.conf.urls import patterns, url
from stagings.views import IndexView, StagingDetailView, CreateOrderView

urlpatterns = patterns('',
  url(r'^$', IndexView.as_view(), name='index'),
  url(r'^(?P<pk>\d+)$', StagingDetailView.as_view(), name='detail'),
  url(r'^create_order$', CreateOrderView.as_view(), name='create_order'),
)
