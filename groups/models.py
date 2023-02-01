"""
Group models.
"""
import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model


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
    admins = models.ManyToManyField('Admin',
                                    related_name="group_admin")
    members = models.ManyToManyField(get_user_model(),
                                     related_name="group_member")

    def __str__(self):
        return self.group_name


class Admin(models.Model):
    """Admin model"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )


class Image(models.Model):
    """Image model"""
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    created_on = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    description = models.CharField(blank=True, max_length=500)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
