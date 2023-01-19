"""
Tests for group admin operations
"""
from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from groups import models

def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class TestGroupAdmin(TestCase):
    """Tests group management by admin"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(self.user)

        defaults = {
            'created_by': self.user.email,
            'group_name': 'Test group name',
            'description': 'Sample group description',
        }

        self.client.post('/api/groups/', defaults)
        self.group = models.Group.objects.get(user=self.user)

    def test_admin_can_add_members_to_group(self):
        """Tests admin can add members to a group"""
        user2 = create_user(
            email='user2@example.com',
            password='password123'
        )
        unauthorized_client = APIClient()
        unauthorized_client.force_authenticate(user2)
        res = self.client.put(
            '/api/groups/1/', {'members': [user2.id]}, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.group.refresh_from_db()
        self.assertTrue(self.group.members.contains(user2))
    






