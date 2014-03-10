from django.contrib import admin
from stagings.models import Zone, Author, Genre, Staging, Piece, VacantZoneSeat


class VacantZoneSeatInlice(admin.TabularInline):
  model = VacantZoneSeat

class StagingAdmin(admin.ModelAdmin):
  fields = ('piece', 'date')
  inlines = (VacantZoneSeatInlice, )
  list_filter = ('date',)
  list_display = ('piece', 'date')

admin.site.register(Zone)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Piece)
admin.site.register(Staging, StagingAdmin)
