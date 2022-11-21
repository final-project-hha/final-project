from django.contrib.auth.models import User
from django.db import models


class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=150)
    django_user = models.OneToOneField(User, on_delete=models.CASCADE)


class Profile(models.Model):
    avatar = models.URLField()
    about_me = models.TextField()
    settings = models.JSONField()
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name="profile")
