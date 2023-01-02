
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Post
from instagram.serializers import PostSerializer,DetailPostSerializer
import os
import tempfile
from PIL import Image

POST_URL = reverse('instagram:post-list')


def detail_url(post_id):
    """Create and return detail_url for a post."""
    return reverse('instagram:post-detail',args=[post_id])

def create_user(**params):
    """Create and return an user."""
    return get_user_model().objects.create_user(**params)

def image_upload_url(post_id):
    """Create and return an image upload URL."""
    return reverse('instagram:post-upload-image', args=[post_id])


def create_post(user, **params):
    """Create and return a post."""
    defaults = {
        'description':'sample title',
    }
    defaults.update(params)

    post = Post.objects.create(author=user, **defaults)
    return post

class PublicPostAPITests(TestCase):
    """Test unauthenticated API request """
    def setUp(self):
        self.clint = APIClient()


    def test_auth_requred(self):
        res = self.clint.get(POST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivatePostAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='abc@example.com',password='abc123')
        self.client.force_authenticate(self.user)


    def test_retrive_post(self):
        """Test for retrieving a post."""
        create_post(user=self.user)
        create_post(user=self.user)

        respone = self.client.get(POST_URL)
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        
        self.assertEqual(respone.status_code, status.HTTP_200_OK)
        self.assertEqual(respone.data, serializer.data)

    def test_create_post(self):
        """Test creating a post."""
        payload = {
            'description': 'Sample post',
        }
        respone = self.client.post(POST_URL, payload)

        self.assertEqual(respone.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(id=respone.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(post, k), v)
        self.assertEqual(post.author, self.user)

    def test_get_post_detail(self):
        """Test for detail a post."""
        post = create_post(user=self.user)
        url = detail_url(post.id)
        respone = self.client.get(url)

        serializer = DetailPostSerializer(post)
        self.assertEqual(respone.data, serializer.data)

    def test_partial_updates(self):
        """Test patch a post."""
        post = create_post(
            user = self.user,
            description = 'Sample description',  
        )
        payload = {'description':'New post description'}
        url = detail_url(post.id)
        res = self.client.patch(url, payload)
    
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.description, payload['description'])
        self.assertEqual(post.author, self.user)

    def test_full_update(self):
        """Test all update for a post"""
        post = create_post(
            user=self.user,
            description='Sample post description',
        )
        payload = {
            'description': 'New post description',
        }
        url = detail_url(post.id)
        response = self.client.put(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()

        for k, v in payload.items():
            self.assertEqual(getattr(post, k), v)
        self.assertEqual(post.author, self.user)


    def test_post_delete(self):
        """Test delete a post"""
        post = create_post(user=self.user)
        url = detail_url(post.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=post.id).exists())



class ImageUploadTests(TestCase):
    """Tests for the image upload API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='abc@example.com',password='abc123')
        self.client.force_authenticate(self.user)
        self.post = create_post(user=self.user)

    def tearDown(self):
        self.post.photo.delete()

    def test_upload_image(self):
        """Test uploading an image to a post."""
        url = image_upload_url(self.post.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'photo': image_file,'description':'description 1'}
            response = self.client.post(url, payload, format='multipart')
           
        self.post.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('photo', response.data)
        self.assertTrue(os.path.exists(self.post.photo.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image."""
        url = image_upload_url(self.post.id)
        payload = {'photo': 'notanimage'}
        response = self.client.post(url, payload, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
