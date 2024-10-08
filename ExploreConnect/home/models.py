from django.db import models


# Create your models here.
class AudioModel(models.Model):
    audioname=models.CharField(max_length=500)
    audio=models.FileField(upload_to='audio')

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    continent = models.CharField(max_length=100)
    slideshow_images = models.ManyToManyField('SlideshowImage', related_name='destinations', blank=True)

    def __str__(self):
        return self.name


class SlideshowImage(models.Model):
    image = models.ImageField(upload_to='slideshow_images/')
    alt_text = models.CharField(max_length=100)

    def __str__(self):
        return self.alt_text


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
