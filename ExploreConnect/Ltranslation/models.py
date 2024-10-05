from django.db import models

# Create your models here.
class AudioModel(models.Model):
    audioname=models.CharField()
    audio=models.FileField(upload_to='audio')