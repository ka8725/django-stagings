from django.contrib import admin
from stagings import models


class StagingZoneInline(admin.TabularInline):
  model = models.StagingZone


class StagingAdmin(admin.ModelAdmin):
  fields = ('piece', 'date')
  inlines = (StagingZoneInline, )
  list_filter = ('date',)
  list_display = ('piece', 'date')


class LineItemInline(admin.TabularInline):
  model = models.LineItem


class OrderAdmin(admin.ModelAdmin):
  inlines = (LineItemInline, )


admin.site.register(models.Zone)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Author)
admin.site.register(models.Genre)
admin.site.register(models.Piece)
admin.site.register(models.Staging, StagingAdmin)
