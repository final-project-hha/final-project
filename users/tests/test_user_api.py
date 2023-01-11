"""
Tests for the user API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status

from rest_framework.test import APIClient

payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test name',
        }


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Test the public features of the user API """
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test that creating a user is successful"""
        res = self.client.post('/api/users/', payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        create_user(**payload)
        res = self.client.post('/api/users/', payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
