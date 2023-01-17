"""
Tests for group API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from groups import models


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

    def test_authentication_required_401_UNAUTHORIZED(self):
        """Test authentication is required to call group API."""
        res = self.client.get('/api/groups/')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateGroupApi(TestCase):
    """Test Authenticated API requests."""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123',
        )
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

    def test_authenticated_user_can_create_a_group(self):
        """Test user can create a group."""
        payload = {
            'group_name': 'Test group name',
            'description': 'Sample group description',
        }
        res = self.client.post('/api/groups/', payload)

        group = models.Group.objects.get(pk=1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['group_name'], group.group_name)

    def test_user_creator_set_as_an_admin(self):
        """Test user can create a group."""
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

    def test_group_was_added_to_admin(self):
        """Test create a group add a group id
            in the admin instance."""
        payload = {
            'group_name': 'Test group name',
            'description': 'Sample group description',
        }
        res = self.client.post('/api/groups/', payload)

        group = models.Group.objects.get(user=self.user)
        admin = models.Admin.objects.get(user=self.user)
        groups_in_admin = admin.groups.all()
        self.assertIn(admin.pk, res.data['admins'])
        self.assertEqual(groups_in_admin[0], group)
