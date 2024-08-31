from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=100)
    continent = models.CharField(max_length=100)
    country_discription = models.TextField()

    def __str__(self):
        return self.name
class DestinationDetails(models.Model):
    destination = models.OneToOneField(Destination, on_delete=models.CASCADE, related_name='details')
    description = models.TextField()
    images = models.JSONField()  # Stores image URLs or paths as a list of strings
    cultural_insights = models.TextField()
    popular_accommodations = models.TextField()
    accommodation_images = models.JSONField()  # Stores accommodation images as a list of URLs or paths
    dining_options = models.TextField()
    dining_images = models.JSONField()  # Stores dining images as a list of URLs or paths

    def __str__(self):
        return f"Details for {self.destination.name}"
