"""
Tests for the group model.
"""
import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from groups.models import Group


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email, password)


class GroupModelTests(TestCase):
    """Test for the model group"""

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
