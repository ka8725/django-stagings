from django import template
from stagings import models

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


def _seats_for_zone(user, staging_zone, status):
  orders = models.Order.objects.filter(user=user, status=status).all()
  line_items = models.LineItem.objects.filter(
    zone=staging_zone.zone,
    order__in=orders,
  )
  return sum(line_item.quantity for line_item in line_items)


def _tickets_sum(user, zones, status):
  orders = models.Order.objects.filter(user=user, status=status).all()
  line_items = models.LineItem.objects.filter(
    zone__in=zones,
    order__in=orders,
  )
  return sum(line_item.total for line_item in line_items)
