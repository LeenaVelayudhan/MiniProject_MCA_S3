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
    images = models.ImageField(upload_to='destination_images/')  # Stores a single image path or URL
    cultural_insights = models.TextField()

    def __str__(self):
        return f"Details for {self.destination.name}"

class Accommodation(models.Model):
    destination_details = models.ForeignKey(DestinationDetails, on_delete=models.CASCADE, related_name='accommodations')
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='accommodation_images/')

    def __str__(self):
        return self.name

class DiningOption(models.Model):
    destination_details = models.ForeignKey(DestinationDetails, on_delete=models.CASCADE, related_name='dining_options')
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='dining_images/')

    def __str__(self):
        return self.name
