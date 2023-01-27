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
        # ______Creating a first user,
        # who creates a group and becomes Admin_____
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

        # _______Creating a second user, not admin______________

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

        res = self.unauthorized_client.post(
            '/api/groups/1/add_member/users/2/')

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
        self.assertEqual(len(res.data['admins'])+len(res.data['members']), 3)

    def test_get_list_of_group_users_in_the_case_there_are_no_members(self):
        """Test if there is no member on the group retrieve only admins."""
        res = self.client.get('/api/groups/1/members/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['admins']), 1)

    def test_remove_members_from_group(self):
        """Tests remove members from a group"""
        self.client.post('/api/groups/1/add_member/users/2/')

        res = self.client.delete('/api/groups/1/members/2/')

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(self.user2, self.group.members.all())
        self.assertTrue(self.user2)

    def test_only_admin_can_remove_member_from_group(self):
        """Tests only admin can remove member from group"""
        # making user 2 a group member
        self.client.post('/api/groups/1/add_member/users/2/')

        # creating user 3, adding to group and using to delete member 2
        user3 = create_user(email="user3@example.com", password="password123")
        self.unauthorized_client.force_authenticate(user3)
        self.client.post('/api/groups/1/add_member/users/3/')
        res = self.unauthorized_client.delete('/api/groups/1/members/2/')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn(self.user2, self.group.members.all())

    def test_making_a_member_an_admin(self):
        """Tests making a member an admin"""
        # making user 2 a group member
        self.client.post('/api/groups/1/add_member/users/2/')

        res = self.client.patch('/api/groups/1/members/2/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        is_admin = self.group.admins.filter(user_id=self.user2.id).exists()
        self.assertTrue(is_admin)
        self.assertFalse(self.group.members.filter(id=self.user2.id).exists())

    def test_only_admin_can_make_a_member_an_admin(self):
        """Tests that only admins can make a member"""
        # making user 2 a group member
        self.client.post('/api/groups/1/add_member/users/2/')

        res = self.unauthorized_client.patch('/api/groups/1/members/2/')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        is_admin = self.group.admins.filter(user_id=self.user2.id).exists()
        self.assertFalse(is_admin)

    def test_admin_can_become_a_member_and_lose_admin_status(self):
        """Test that admin can become a member"""
        # making user 2 a member of group 1
        self.client.post('/api/groups/1/add_member/users/2/')
        # making member 2 an admin
        self.client.patch('/api/groups/1/members/2/')
        # turning admin 2 back into member
        res = self.client.patch('/api/groups/1/members/2/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        is_member = self.group.members.filter(id=self.user2.id)
        self.assertTrue(is_member)
