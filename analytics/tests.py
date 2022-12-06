from django.test import TestCase

from django.test import TestCase
from rest_framework.test import APIClient

from analytics.models import Counter


def create_counter():
    return Counter.objects.create(name='Counter')


class TestCounterMiddleWare(TestCase):
    def setUp(self):
        self.client = APIClient()
        create_counter()

    def test_counter_middleware_if_count_each_time_endpoint_is_accessed(self):
        self.client.get('/api/v1/members/')
        counter = Counter.objects.first()
        self.assertEqual(counter.counter, 1)
