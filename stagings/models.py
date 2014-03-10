from django.db import models


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

  def __unicode__(self):
    return self.name


class Staging(models.Model):
  piece = models.ForeignKey(Piece)
  date = models.DateField()

  def __unicode__(self):
    return '%s: %s' % (self.piece.name, self.date)


class VacantZoneSeat(models.Model):
  zone = models.ForeignKey(Zone)
  staging = models.ForeignKey(Staging)
  total = models.PositiveSmallIntegerField()
