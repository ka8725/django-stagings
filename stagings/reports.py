from django.db.models import Sum
from stagings.models import Zone, Order

class ZonesReport(object):
  def __init__(self):
    self._report = []
    for zone in Zone.objects.all():
      self._report.append({
        'zone': zone,
        'total_tickets': self._total_tickets(zone),
        'last_tickets': self._last_tickets(zone),
        'ordered_tickets': self._ordered_tickets(zone),
        'paid_tickets': self._paid_tickets(zone),
        'earnings': self._earnings(zone),
      })
    self._report.append({
      'total_earning': self._total_earnings(self._report),
    })

  @property
  def report(self):
    return self._report

  def _total_tickets(self, zone):
    return sum(zone.total_seats for zone in zone.stagingzone_set.all())

  def _last_tickets(self, zone):
    return zone.stagingzone_set.aggregate(Sum('available_seats'))['available_seats__sum']

  def _ordered_tickets(self, zone):
    return sum(map(lambda (_, lineitem): lineitem.quantity,
                self._stagingzone_and_lineitem(zone, Order.NEW)))

  def _paid_tickets(self, zone):
    return sum(map(lambda (_, lineitem): lineitem.quantity,
                self._stagingzone_and_lineitem(zone, Order.PAID)))

  def _earnings(self, zone):
    return sum(map(lambda (zone, lineitem): zone.ticket_price * lineitem.quantity,
                self._stagingzone_and_lineitem(zone, Order.PAID)))

  def _stagingzone_and_lineitem(self, zone, order_status):
    for stagingzone in zone.stagingzone_set.all():
      for lineitem in stagingzone.lineitem_set.filter(
                        order__status=order_status
                      ).all():
        yield(stagingzone, lineitem)

  def _total_earnings(self, zones_report):
    return sum(zone_report['earnings'] for zone_report in zones_report)
