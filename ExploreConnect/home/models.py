from django.db import models

# Create your models here.
class Destination(models.Model):
    name=models.CharField(max_length=150)
    continent=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    description=models.TextField()
    image=models.ImageField()
    culturalinsights=models.TextField()
    accomodations=models.TextField()
    accimgs=models.ImageField()
    dining=models.TextField()
    diningimgs=models.ImageField()
def __str__(self):
        return self.name