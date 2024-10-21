from django.db import models

# Define the Destination model
class Destination(models.Model):
    destination_name = models.CharField(max_length=255, default="Unknown Destination")
    href = models.CharField(max_length=255, default='/')  # Assuming this is the URL without leading/trailing slashes
    destination_description = models.TextField(null=True, blank=True)
    country_name = models.CharField(max_length=255 , default="Unknown Country")
    country_description = models.TextField(null=True, blank=True)
    continent_name = models.CharField(max_length=255,  default="Unknown Continent")
    continent_description = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.destination_name

# Define the BestTimeToVisit model
class BestTimeToVisit(models.Model):
    destination = models.OneToOneField(Destination, on_delete=models.CASCADE, related_name='best_time_to_visit')
    title = models.CharField(max_length=255)
    header_image = models.URLField(null=True, blank=True)
    intropara = models.TextField(null=True, blank=True)
    sections = models.JSONField(null=True, blank=True)  # JSON field to store structured data

    def __str__(self):
        return self.title

# Define the Attraction model
class Attraction(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='attractions')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


# Create your models here.
class AudioModel(models.Model):
    audioname=models.CharField(max_length=500)
    audio=models.FileField(upload_to='audio')





