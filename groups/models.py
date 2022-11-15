from django.contrib.auth.models import User
from django.db import models

from documents.models import Documents
from photos.models import Photos


class Group(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING) # only after the import, it will check the name that's in quotes
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    photo = models.ForeignKey(Photos, null=True, on_delete=models.DO_NOTHING)
    # document = models.ForeignKey(Documents, null=True)
    members = models.ManyToManyField('users.Member', related_name='groups', blank=True)
    # admins = models.ManyToManyField('users.Member', null=True, on_delete=models.SET_DEFAULT, default=User.admin)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    # photos = models.ForeignKey(Photos, null=True)
    # documents = models.ForeignKey(Documents, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
