from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    house = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    def __str__(self):
        return self.user
