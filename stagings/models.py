from registration.signals import user_activated
from django.dispatch import receiver
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property
from django.contrib.auth.models import User
from stagings import constants
from django.contrib.auth.models import Group


class Author(models.Model):
  name = models.CharField(max_length=255)

  def __unicode__(self):
    return self.name


class Genre(models.Model):
  name = models.CharField(max_length=255)

  def __unicode__(self):
    return self.name


class Piece(models.Model):
  name = models.CharField(max_length=255)
  genre = models.ForeignKey(Genre)
  author = models.ForeignKey(Author)

  def __unicode__(self):
    return self.name


class Zone(models.Model):
  name = models.CharField(max_length=255)
  total_seats = models.PositiveSmallIntegerField()

  def __unicode__(self):
    return self.name


class Staging(models.Model):
  piece = models.ForeignKey(Piece, unique_for_date='date')
  date = models.DateField()

  def is_past(self):
    return self.date < date.today()

  @cached_property
  def zones(self):
    return self.stagingzone_set.all()

  def __unicode__(self):
    return '%s: %s' % (self.piece.name, self.date)


class StagingZone(models.Model):
  zone = models.ForeignKey(Zone)
  staging = models.ForeignKey(Staging)
  ticket_price = models.PositiveSmallIntegerField()
  available_seats = models.PositiveSmallIntegerField()

  @property
  def total_seats(self):
    return self.zone.total_seats

  def clean(self):
    if not self.available_seats and self.zone:
      self.available_seats = self.total_seats

    if self.available_seats < 0:
      raise ValidationError('Available seats can not be negative number.')

    if self.available_seats > self.zone.total_seats:
      raise ValidationError('Available seats can not be greater than total seats for zone.')

  def __unicode__(self):
    return self.zone


class Order(models.Model):
  NEW = 0
  PAID = 1
  STATUSES = (
    (NEW, 'New'),
    (PAID, 'Paid')
  )

  user = models.ForeignKey(User)
  total = models.PositiveSmallIntegerField()
  status = models.PositiveSmallIntegerField(choices=STATUSES, default=NEW)
  date = models.DateField()

  def delete(self):
    self._revert_zone_seats()
    super(Order, self).delete()

  def pay(self):
    self.status = self.PAID
    self.save()

  def _revert_zone_seats(self):
    for line_item in self.lineitem_set.all():
      line_item.zone.available_seats += line_item.quantity
      line_item.zone.save()


class LineItem(models.Model):
  order = models.ForeignKey(Order)
  quantity = models.PositiveSmallIntegerField(default=0)
  zone = models.ForeignKey(StagingZone)

  @property
  def total(self):
    return (self.quantity or 0) * self.zone.ticket_price

  def __unicode__(self):
    return '%s - %s' % (self.zone.zone, self.quantity)


@receiver(user_activated)
def add_user_to_clients_group(sender, **kwargs):
  clients_group, _ = Group.objects.get_or_create(
    name=constants.CLIENTS_GROUP
  )
  kwargs['user'].groups.add(clients_group)
