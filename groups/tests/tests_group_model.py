"""
Tests for the group model.
"""
import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from groups.models import Group, Admin


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email, password)


class GroupModelTests(TestCase):
    """Tests for the model group"""

    def test_create_a_group(self):
        """Test Creating a group successful."""
        user = create_user()
        group = Group.objects.create(
            user=user,
            created_by=user.email,
            group_name='Sample group name.',
            description='Sample description.',
        )
        self.assertEqual(str(group), group.group_name)
        self.assertEqual(group.created_on,
                         datetime.datetime.now().strftime('%Y-%m-%d %H:%m'))
        self.assertEqual(group.members.count(), 0)


class AdminModelTests(TestCase):
    """Tests for the model admin"""
    def setUp(self):
        self.user = create_user()
        self.group = Group.objects.create(
            user=self.user,
            created_by=self.user.email,
            group_name='first_group',
            description='this is the first group'
        )

    def test_create_admin(self):
        """Tests creating admin successful"""
        admin = Admin.objects.create(
            user=self.user,
        )

        admin.group_admin.set([self.group.pk])
        group1 = admin.group_admin.get(pk=1)
        self.assertEqual(group1.group_name, self.group.group_name)
        self.assertEqual(admin.group_admin.count(), 1)
