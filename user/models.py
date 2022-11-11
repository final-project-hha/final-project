# questions:
#how to add a "joined_on" field to each group that this user is a member of?
#where should the roles of a user in a group be defined? in the user or in the group?
#add memebers field to group


from django.contrib.auth.models import User
from django.db import models

from group.models import Group


class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=150)
    django_user = models.OneToOneField(User, on_delete=models.CASCADE)
    member_of = models.ForeignKey(Group, related_name="group", null=True, on_delete=models.SET_NULL)


class Profile(models.Model):
    avatar = models.URLField()
    about_me = models.TextField()
    settings = models.JSONField()
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name="profile")





