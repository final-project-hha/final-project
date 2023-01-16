"""
Tests for group API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from groups import models
from groups.serializers import GroupSerializer


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


def create_group(user, **params):
    """Create and return a new group."""
    defaults = {
        'created_by': user.email,
        'group_name': 'Test group name',
        'description': 'Sample group description',
    }
    defaults.update(params)

    group = models.Group.objects.create(user=user, **defaults)
    return group


class PublicGroupApi(TestCase):
    """Test unauthenticated API requests."""
    def setUp(self):
        self.client = APIClient()

    def test_authentication_required_401_ERrOR(self):
        """Test authentication is required to call group API."""
        res = self.client.get('/api/groups/')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateGroupApi(TestCase):
    """Test Authenticated API requests."""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='testpass123')
        self.client.force_authenticate(self.user)

    def test_creating_a_group_201_CREATED(self):
        """Test creating a group."""
        payload = {
            'group_name': 'Test group name',
            'description': 'Sample group description',
        }
        res = self.client.post('/api/groups/', payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        group = models.Group.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(group, k), v)
        self.assertEqual(group.user, self.user)

    def test_creating_a_group_set_the_creator_user_as_admin(self):
        """Test creating a group set the creator user as admin and created_by."""
        payload = {
            'group_name': 'Test group name',
            'description': 'Sample group description',
        }
        res = self.client.post('/api/groups/', payload)

        group = models.Group.objects.get(id=res.data['id'])
        admin = group.admins.get(pk=1)
        self.assertEqual(self.user, admin.user)
        self.assertEqual(group, admin.groups.get(pk=1))
        self.assertEqual(res.data['created_by'], self.user.email)

    # def test_get_group_details(self):
    #     """Test get group details."""
    #     group = create_group(user=self.user)
    #
    #     res = self.client.get(f'^groups/{group.id}/$')
    #
    #     serializer = GroupSerializer(group)
    #     self.assertEqual(res, serializer.data)


    # def test_admin_of_a_group_can_delete_a_group(self):
    #     """Test admin can destroy a group."""
    #     payload = {
    #         'group_name': 'Test group name',
    #         'description': 'Sample group description',
    #     }
    #     group = create_group(user=self.user, **payload)
    #
    #     res = self.client.delete('/api/groups/', args=1)
    #
    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(group.exists())
