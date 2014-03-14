from django.contrib import admin
from stagings.models import Zone, Author, Genre, Staging, Piece, StagingZone, Order


class StagingZoneInlice(admin.TabularInline):
  model = StagingZone

class StagingAdmin(admin.ModelAdmin):
  fields = ('piece', 'date')
  inlines = (StagingZoneInlice, )
  list_filter = ('date',)
  list_display = ('piece', 'date')

admin.site.register(Zone)
admin.site.register(Order)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Piece)
admin.site.register(Staging, StagingAdmin)
