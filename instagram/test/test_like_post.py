from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Post



def detail_url(post_id):
    return reverse('instagram:like',args=[post_id])

def create_user(**params):
    return get_user_model().objects.create_user(**params)




class PublicLikeAPITests(TestCase):
    """Test unauthenticated API request """
    def setUp(self):
        self.clint = APIClient()


    # def test_auth_requred(self):
    #     res = self.clint.get(POST_URL)

    #     self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateLikeAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='abc@example.com',password='abc123')
        self.client.force_authenticate(self.user)


    def test_like_post(self):
        post = Post.objects.create(author=self.user,description='something')
        url = detail_url(post.id)
        lc = post.number_of_likes()
        #print('likelcccccccc',lc)
        res = self.client.get(url)
        #print(res.data)
        lc = post.number_of_likes()
        #print('likelccccccccccccc',lc)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(lc, 1)