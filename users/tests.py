from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from users.models import Member


# Create your tests here.


def create_user():
    django_user = User.objects.create_user(username='test_user', email='test@test.com', password='1234')
    member = Member.objects.create(first_name='test', last_name='testtest', email='test@test', password='123',
                                   django_user=django_user)

    return member


class TestCaseMemberAPIViewSet(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_user()

    def setUpClass(self):
        self.client = APIClient()
        self.client.login(username='test_user', password='1234')

    def test_list_members_if_is_authenticated_200(self):
        response = self.client.get('/api/v1/members/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_members_if_is_not_authenticated_403(self):
        self.client.logout()
        response = self.client.get('/api/v1/members/')
        self.assertEqual(response.status_code, 403)
