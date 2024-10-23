from django.db import models
from django.contrib.auth.models import User
class Traveler(models.Model):
   
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=20,unique=True)
    password=models.CharField(max_length=25,null=True)
    user=models.OneToOneField(User,related_name='student_profile',on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name} ({self.email})"


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    forget_password_token=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    
