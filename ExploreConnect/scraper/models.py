from django.db import models

class Continent(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.URLField()
    url = models.URLField()

    def __str__(self):
        return self.name

class Attraction(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

class Accommodation(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()


class Destination(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
