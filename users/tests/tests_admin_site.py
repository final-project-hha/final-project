"""
Tests for the admin site.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from django.test import Client


# class AdminSiteTests(TestCase):
#     """Tests for Django Admin."""
#     def setUp(self):
#         """Create user and client."""
#         self.client = Client()
#         self.admin_user = get_user_model().objects.create_superuser(
#             email='admin@example.com',
#             password='testpass123',
#         )
#         self.client.force_login(self.admin_user)
#         self.user = get_user_model().objects.create_user(
#             email='user@example.com',
#             password='testpass123',
#             name='Test User'
#         )
#
#     def test_users_list(self):
#         """Test that users are listed in admin site."""
#         res = self.client.get('/admin/')
#
#         self.assertContains(res, self.user.name)
#         self.assertContains(res, self.user.email)




