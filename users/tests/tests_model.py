"""
Test for the custom user model.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTests(TestCase):
    """Test User"""
    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


