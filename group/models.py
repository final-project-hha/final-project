from django.db import models


class Group(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.Member', null=True, on_delete=models.DO_NOTHING) # only after the import, it will check the name that's in quotes
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    # photos = models.ForeignKey(Photos, null=True)
    # documents = models.ForeignKey(Documents, null=True)


class Event(models.Model):
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    # photos = models.ForeignKey(Photos, null=True)
    # documents = models.ForeignKey(Documents, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


