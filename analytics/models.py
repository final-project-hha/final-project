from django.db import models


# Create your models here.
class Counter(models.Model):
    name = models.CharField(max_length=100)
    counter = models.IntegerField(blank=True)
