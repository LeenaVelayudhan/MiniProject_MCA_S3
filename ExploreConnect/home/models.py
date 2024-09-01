from django.db import models

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
    CATEGORY_CHOICES = [
        ('historical', 'Historical Places'),
        ('food', 'Popular Foods'),
        ('restaurant', 'Restaurants'),
        ('national_park', 'National Parks'),
        ('popular_places', 'Popular Places'),
        ('festival', 'Local Festivals'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='attractions/')
    destination = models.ForeignKey(Destination, related_name='attractions', on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    category_description = models.TextField(default="No description provided")
    category_image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name
