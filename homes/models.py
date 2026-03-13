from django.db import models

# Create your models here.
class Apartment(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    contact = models.CharField(max_length=20)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
