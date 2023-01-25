"""
Event model.
"""
from django.conf import settings
from django.db import models

from groups.models import Group


class Event(models.Model):
    """Event model."""
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name
