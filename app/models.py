from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    color = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    quality = models.CharField(max_length=20)
    price = models.IntegerField()
    category = models.CharField(max_length=50)