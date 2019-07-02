from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User  #username , password , email
from datetime import datetime    
import pytz
from django.utils import timezone

class UserPoints(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

class UserLog(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now())
    InEx = models.TextField(default="Income")
    points = models.IntegerField(default="0")
    package_id = models.TextField(default="-")

class Package(models.Model):
    package_id = models.TextField(primary_key=True)
    name = models.TextField(unique=True,default="")
    type = models.TextField()
    points = models.IntegerField()
    material = models.TextField(default="Plastic")    # Plastic , Aluminium, Metal