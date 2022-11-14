from django.contrib.auth.models import User
from django.db import models


class Photos(models.Model):
    name = models.CharField(max_length=50)
    posted_on = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)