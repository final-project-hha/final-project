"""
Test for the event api
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status

from rest_framework.test import APIClient

from groups import models
from events.models import Event


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicEventAPI(TestCase):
    """Test unauthenticated API requests."""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(self.user)
        group_data = {
            'created_by': self.user.email,
            'group_name': 'Test group name',
            'description': 'Sample group description',
        }
        self.client.post('/api/groups/', group_data)

    def test_authentication_required_for_get_events_401_UNAUTHORIZED(self):
        """Test authentication is required to call event API."""
        res = APIClient().get('/api/groups/1/events/')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateEventAPI(TestCase):
    """Test authenticate API event requests."""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(self.user)
        group_data = {
            'created_by': self.user.email,
            'group_name': 'Test group name',
            'description': 'Sample group description',
        }
        self.client.post('/api/groups/', group_data)
        self.group = models.Group.objects.get(user=self.user)

    def create_event(self, **params):
        """Test Create an event."""
        defaults = {
            'name': 'Event title',
            'description': 'Sample description event',
            'start_time': '2023-01-01 10:30',
            'end_time': '2023-01-01 18:00',
            'location': 'Reichstag',
        }
        defaults.update(params)
        self.client.post('/api/group/1/add_event/', defaults)

    def test_creating_a_event_by_admin_201_CREATED(self):
        """Test Creating an event with an associated group"""
        payload = {
            'name': 'Event title',
            'description': 'Sample description event',
            'start_time': '2023-01-01 14:12:00.000000',
            'end_time ': '2023-01-01 18:00:00.000000',
            'created_by': self.user,
            'location ': 'Reichstag',
        }
        res = self.client.post('/api/group/1/add_event/', payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        event = Event.objects.filter(id=res.data['id'])
        self.assertTrue(event.exists())
        self.assertEqual(event[0].group, self.group)

    def test_members_can_add_event_201_CREATED(self):
        """Test members of a group can create an event."""

        payload = {
            'name': 'Event title',
            'description': 'Sample description event',
            'start_time': '2023-01-01 14:12:00.000000',
            'end_time ': '2023-01-01 18:00:00.000000',
            'created_by': self.user,
            'location ': 'Reichstag',
        }
        user2 = create_user(email='user2@example.com', password='testpass123')
        unauthorized_client = APIClient()
        unauthorized_client.force_authenticate(user2)
        self.client.post('/api/groups/1/add_member/users/2/')
        res = unauthorized_client.post('/api/group/1/add_event/', payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        event = Event.objects.filter(id=res.data['id'])
        self.assertTrue(event.exists())
        self.assertEqual(event[0].group, self.group)

    def test_only_members_or_admins_in_group_can_create_an_event(self):
        """Only member and admins in a group
         can create events in the respective group."""
        payload = {
            'name': 'Event title',
            'description': 'Sample description event',
            'start_time': '2023-01-01 14:12:00.000000',
            'end_time ': '2023-01-01 18:00:00.000000',
            'location ': 'Reichstag',
        }
        user2 = create_user(email='user2@example.com', password='testpass123')
        unauthorized_client = APIClient()
        unauthorized_client.force_authenticate(user2)

        res = unauthorized_client.post('/api/group/1/add_event/', payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_group_members_get_list_of_group_events(self):
        """Test member of a group can get a list of group events."""
        self.create_event()
        self.create_event(**{'name': 'Event2'})

        res = self.client.get('/api/groups/1/events/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_people_not_in_the_group_cant_see_events(self):
        """Test users can only get list of events
        if they belong to the group."""
        self.create_event()
        self.create_event(**{'name': 'Event2'})

        user2 = create_user(email='user2@example.com', password='testpass123')
        unauthorized_client = APIClient()
        unauthorized_client.force_authenticate(user2)

        res = unauthorized_client.get('/api/groups/1/events/')

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieving_an_event_by_id(self):
        """Test retrieve an event details."""
        self.create_event()
        self.create_event(**{'name': 'Event2'})

        res = self.client.get('/api/group/1/events/1/event_details/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], 'Event title')

    def test_retrieving_an_event_by_id_only_for_members_and_admins(self):
        """Test Only members and admins of a group
         can get details of a specific event."""
        self.create_event()

        user2 = create_user(email='user2@example.com', password='testpass123')
        unauthorized_client = APIClient()
        unauthorized_client.force_authenticate(user2)

        res = unauthorized_client.get('/api/group/1/events/1/event_details/')

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

