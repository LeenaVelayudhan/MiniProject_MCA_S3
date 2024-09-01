# admin.py
from django.contrib import admin
from .models import Destination, SlideshowImage, Attraction

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'continent', 'description')
    search_fields = ('name', 'description')
    filter_horizontal = ('slideshow_images',)  # For ManyToManyField

@admin.register(SlideshowImage)
class SlideshowImageAdmin(admin.ModelAdmin):
    list_display = ('alt_text', 'image')
    search_fields = ('alt_text',)

@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description', 'destination')
    search_fields = ('name', 'description')
    list_filter = ('category', 'destination')
