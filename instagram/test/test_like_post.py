from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Post



def detail_url(post_id):
    """Create and return detail_url for a post."""
    return reverse('instagram:like',args=[post_id])

def create_user(**params):
    """Create and return an user."""
    return get_user_model().objects.create_user(**params)


class PublicLikeAPITests(TestCase):
    """Test unauthenticated API request """
    def setUp(self):
        self.clint = APIClient()


class PrivateLikeAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='abc@example.com',password='abc123')
        self.client.force_authenticate(self.user)


    def test_like_post(self):
        """Test likes"""
        post = Post.objects.create(author=self.user,description='something')
        url = detail_url(post.id)
        lc = post.number_of_likes()
        res = self.client.get(url)
        lc = post.number_of_likes()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(lc, 1)