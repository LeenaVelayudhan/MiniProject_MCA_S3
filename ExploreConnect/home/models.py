
# models.py
from django.db import models

class Destination(models.Model):
    destination_name = models.CharField(max_length=255)
    country_name = models.CharField(max_length=255)
    continent_name = models.CharField(max_length=255)
    continent_description = models.TextField()
    destination_description = models.TextField()
    image_url = models.URLField()
    weather_data = models.JSONField(null=True, blank=True)  # To store weather data

    def __str__(self):
        return f"{self.destination_name}, {self.country_name}"


# Create your models here.
class AudioModel(models.Model):
    audioname=models.CharField(max_length=500)
    audio=models.FileField(upload_to='audio')





class Attraction(models.Model):
    destination = models.ForeignKey(Destination, related_name='attractions', on_delete=models.CASCADE)
    CATEGORY_CHOICES = [
        ('Historical Places','Harmony between Tradition and Modernity'),
        ('Foods & Restaurants ','Gourmet Travel'),
        ('Nature','Nature and Its Healing Power'),
        ('Activities','Travel Activities'),
        ('Popular places','Popular places (attractions)'),
        ('Local festivals','Local Festivals'),
        
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='attractions/')

    def __str__(self):
        return self.name
