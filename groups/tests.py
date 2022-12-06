from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from groups.models import Group
from users.models import Member


def generate_data():
    django_user = User.objects.create_user(username='django', email='test@test.com', password='test')
    member = Member.objects.create(first_name="Bunny", last_name="Bugs", email='test@test.com', password='test', user=django_user)

    group = Group.objects.create(created_by=django_user, name='Bunny\'s group', password='test', description='Bunny is amazing')
    # admin = group.admins.add(member, role='AD')


class TestGroup(TestCase):

    def SetUp(self):
        generate_data()

    def test_group_created_on_field(self):
        group = Group.objects.first()

        self.assertEqual(group.created_on.date, datetime.datetime.now().date())




