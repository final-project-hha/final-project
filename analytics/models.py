from django.db import models


class Counter(models.Model):
    name = models.CharField(max_length=100)
    counter = models.IntegerField(default=0)
