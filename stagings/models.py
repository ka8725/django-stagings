from django.db import models
from datetime import date
from django.core.exceptions import ValidationError


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
  piece = models.ForeignKey(Piece)
  date = models.DateField()

  def is_past(self):
    return self.date < date.today()

  def __unicode__(self):
    return '%s: %s' % (self.piece.name, self.date)


class VacantZoneSeat(models.Model):
  zone = models.ForeignKey(Zone)
  staging = models.ForeignKey(Staging)
  ticket_price = models.PositiveSmallIntegerField()
  available_seats = models.PositiveSmallIntegerField()

  def clean(self):
    if not self.available_seats and self.zone:
      self.available_seats = self.zone.total_seats

    if self.available_seats < 0:
      raise ValidationError('Available seats can not be negative number.')

    if self.available_seats > self.zone.total_seats:
      raise ValidationError('Available seats can not be greater than total seats for zone.')
