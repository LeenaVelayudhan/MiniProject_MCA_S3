
# models.py
from django.db import models
from django.db import models

class Continent(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name

class Destination(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE,null=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name



# Create your models here.
class AudioModel(models.Model):
    audioname=models.CharField(max_length=500)
    audio=models.FileField(upload_to='audio')





