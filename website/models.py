from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class History(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="userHistory")
    title = models.CharField(max_length=500, blank=True)
    description = models.CharField(max_length=500, blank=True)
    date = models.CharField(max_length=30, blank=True)
    author = models.CharField(max_length=500, blank=True)
    image = models.CharField(max_length=500, blank=True)
    url = models.CharField(max_length=500, blank=True)
    time = models.DateTimeField(auto_now_add=True) 