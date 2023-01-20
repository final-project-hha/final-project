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
        #______Creating a first user, who creates a group and becomes Admin_____
        self.user = create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        defaults = {
            'created_by': self.user.email,
            'group_name': 'Test group name',
            'description': 'Sample group description',
        }

        self.client.post('/api/groups/', defaults)
        self.group = models.Group.objects.get(user=self.user)

        #_______Creating a second user, not admin______________

        self.user2 = create_user(
            email='user2@example.com',
            password='password123'
        )
        self.unauthorized_client = APIClient()
        self.unauthorized_client.force_authenticate(self.user2)

    def test_add_members_to_group(self):
        """Tests members can be added to a specific group"""
        res = self.client.post(
            '/api/groups/1/add_member/users/2/'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(self.group.members.contains(self.user2))

    def test_only_admin_can_add_members_to_that_group(self):
        """Tests only admin of the group can add members to it"""

        res = self.unauthorized_client.post('/api/groups/1/add_member/users/2/')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(self.group.members.contains(self.user2))

    def test_members_of_group_can_see_all_it_members(self):
        """Tests that members of a group can see its members"""
        self.client.post('/api/groups/1/add_member/users/2/')
        user3 = create_user(email="user3@example.com", password="password123")
        self.unauthorized_client.force_authenticate(user3)
        self.client.post('/api/groups/1/add_member/users/3/')
        res = self.unauthorized_client.get('/api/groups/1/members/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)


