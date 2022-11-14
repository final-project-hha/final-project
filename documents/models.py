from django.db import models

# from users.models import Member


class Documents(models.Model):
    name = models.CharField(max_length=50)
    posted_on = models.DateTimeField(auto_now_add=True)
    # posted_by = models.ForeignKey('users.Member', on_delete=models.DO_NOTHING)
