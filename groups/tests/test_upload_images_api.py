"""
Test for Uploading images in the API
"""
from PIL import Image as PilImage
import tempfile

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status

from rest_framework.test import APIClient

from groups.models import Group, Image


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email, password)


class ImageUploadingTest(TestCase):
    """Test for uploading images in the API"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        group_data = {
            'created_by': self.user.email,
            'group_name': 'Test group name',
            'description': 'Sample group description',
        }
        self.client.post('/api/groups/', group_data)
        self.group = Group.objects.get(user=self.user)

    def tearDown(self):
        image = Image.objects.first()
        image.image.delete()

    def test_uploading_image_successful(self):
        """Test uploading images successful"""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = PilImage.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {
                'name': 'Test_image',
                'image': image_file,
                'description': 'This is a sample description'
            }

            res = self.client.post('/api/group/1/add_image/', payload)

            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            self.assertEqual(len(Image.objects.all()), 1)

    def test_retrieving_image_by_id(self):
        """Test get images by id."""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = PilImage.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {
                'name': 'Test_image',
                'image': image_file,
                'description': 'This is a sample description'
            }

            self.client.post('/api/group/1/add_image/', payload)
            res = self.client.get('/api/group/1/images/1/')

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            image = Image.objects.get(id=1)
            self.assertEqual(res.data['id'], image.id)
