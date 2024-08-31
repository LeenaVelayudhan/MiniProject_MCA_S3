from django.contrib import admin
from .models import Destination,DestinationDetails

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'continent', 'country')
    search_fields = ('name', 'continent', 'country')

@admin.register(DestinationDetails)
class DestinationDetailsAdmin(admin.ModelAdmin):
    list_display = ('destination', 'description')
    search_fields = ('destination__name', 'description')