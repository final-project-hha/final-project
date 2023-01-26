"""
Test for the Event Model.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase

from groups.models import Group
from events.models import Event


class EventModelTests(TestCase):
    """Test for the event model."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpass123',
        )
        self.group = Group.objects.create(
            user=self.user,
            created_by=self.user.email,
            group_name='Sample group name.',
            description='Sample description.',
        )

    def test_create_an_event_in_group(self):
        """Test creating an event in a group successful."""
        event = Event.objects.create(
            group=self.group,
            name='Event title',
            description='Sample description event',
            start_time='2023-01-01,10:30',
            end_time='2023-01-01,18:00',
            created_by=self.user,
            location='Reichstag',
        )
        self.assertEqual(str(event), event.name)
        self.assertEqual(event.created_by, self.user)
        self.assertEqual(event.start_time, '2023-01-01,10:30')
