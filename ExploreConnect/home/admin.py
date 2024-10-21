from django.contrib import admin
from .models import Destination, BestTimeToVisit, Attraction

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('destination_name', 'country_name', 'continent_name')

@admin.register(BestTimeToVisit)
class BestTimeToVisitAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination')

@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination')

