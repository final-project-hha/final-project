"""
Group models.
"""
import datetime

from django.conf import settings
from django.db import models


class Group(models.Model):
    """Group model."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )
    created_by = models.CharField(max_length=255)
    group_name = models.CharField(max_length=255)
    description = models.TextField()
    created_on = models.DateTimeField(
        default=datetime.datetime.now().strftime('%Y-%m-%d %H:%m'))
    admins = models.ManyToManyField('Admin')

    def __str__(self):
        return self.group_name


class Admin(models.Model):
    """Admin model"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )
    groups = models.ManyToManyField(Group, related_name="admin")
