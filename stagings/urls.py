from django.conf.urls import patterns, url
from stagings.views import IndexView
from stagings.views import CreateOrderView
from stagings.views import StagingDetailView

urlpatterns = patterns('',
  url(r'^$', IndexView.as_view(), name='index'),
  url(r'^(?P<pk>\d+)$', StagingDetailView.as_view(), name='detail'),
  url(r'^(?P<pk>\d+)/create_order$', CreateOrderView.as_view(), name='create_order'),
)
