from django import template
from django.db.models import Sum
from stagings import models
from stagings import constants

register = template.Library()


@register.filter
def ordered_seats_for_zone(user, staging_zone):
  return _seats_for_zone(user, staging_zone, models.Order.NEW)


@register.filter
def ordered_tickets_sum(user, zones):
  return _tickets_sum(user, zones, models.Order.NEW)


@register.filter
def paid_seats_for_zone(user, staging_zone):
  return _seats_for_zone(user, staging_zone, models.Order.PAID)


@register.filter
def paid_tickets_sum(user, zones):
  return _tickets_sum(user, zones, models.Order.PAID)


@register.filter
def is_courier(user):
  return user.groups.filter(name=constants.COURIERS_GROUP)


def _seats_for_zone(user, staging_zone, status):
  orders = models.Order.objects.filter(user=user, status=status).prefetch_related('lineitem_set')
  return models.LineItem.objects.filter(
    zone=staging_zone,
    order__in=orders,
  ).aggregate(seats_for_zone=Sum('quantity'))['seats_for_zone']


def _tickets_sum(user, zones, status):
  # TODO: rework for joins to get rid of possible performance issues
  orders = models.Order.objects.filter(user=user, status=status).all()
  line_items = models.LineItem.objects.filter(
    zone__in=zones,
    order__in=orders,
  )
  return sum(line_item.total for line_item in line_items)
