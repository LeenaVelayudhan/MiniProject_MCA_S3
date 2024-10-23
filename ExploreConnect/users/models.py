from django.db import models

class Traveler(models.Model):
   
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=20,unique=True)
    password=models.CharField(max_length=25,null=True)
    user=models.OneToOneField(User,related_name='student_profile',on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name} ({self.email})"
