from datetime import timezone

from django.contrib.auth.models import User
from django.db import models

from documents.models import Documents
from photos.models import Photos
from users.models import Member


def return_admin():
    return [g.id for g in GroupMembers.objects.filter(role='AD')]


class Group(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    photo = models.ForeignKey(Photos, null=True, on_delete=models.DO_NOTHING)
    # document = models.ForeignKey(Documents, null=True)
    # admins = models.ManyToManyField('users.Member', through='GroupMembers', default=return_admin)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    # photos = models.ForeignKey(Photos, null=True)
    # documents = models.ForeignKey(Documents, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


roles_choices = [
    ('AD', 'Admin'),
    ('MR', 'Member')
]


class GroupMembers(models.Model):
    class Meta:
        unique_together = (('group', 'member'),)

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='group_member')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=roles_choices, default='MR')
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.member.first_name} - {self.group.name} - {self.role}'

