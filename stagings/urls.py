from django.conf.urls import patterns, url
from stagings.views import (IndexView,
                            CreateOrderView,
                            StagingDetailView,
                            StagingOrdersView,
                            OrderConfirmationView,
                            CancelOrderView,
                            pay_orders,
                            cancel_orders)

urlpatterns = patterns('',
  url(r'^$',
    IndexView.as_view(),
    name='index'),

  url(r'^(?P<pk>\d+)$',
    StagingDetailView.as_view(),
    name='detail'),

  url(r'^(?P<staging_pk>\d+)/create_order$',
    CreateOrderView.as_view(),
    name='create_order'),

  url(r'^(?P<staging_pk>\d+)/orders$',
    StagingOrdersView.as_view(),
    name='staging_orders'),

  url(r'^(?P<staging_pk>\d+)/orders/(?P<pk>\d+)$',
    OrderConfirmationView.as_view(),
    name='order_confirmation'),

  url(r'^orders/(?P<pk>\d+)$',
    CancelOrderView.as_view(),
    name='cancel_order'),

  url(r'^cancel_orders$',
    cancel_orders,
    name='cancel_orders'),

  url(r'^pay_orders$',
    pay_orders,
    name='pay_orders'),
)
