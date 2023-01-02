from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Comment, Post





def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)


def detail_url(post_id):
    """Create and return detail url for a post."""
    return reverse('instagram:add-comment', args=[post_id])

def manage_comment(c_id):
    """Create and return detail url for a comment."""
    return reverse('instagram:manage-comment',args=[c_id])


class PublicCommentApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_create_comment(self):
        """Test creating a comment for unauthenticated users."""
        post = Post.objects.create(author=create_user(),description='sample des')
        payload = {
            'comment':'hi',
        }
        url = detail_url(post.id)
        response  = self.client.post(url, payload)
        
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['comment'], payload['comment'])


class PrivateCommentApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)



    def test_create_comment(self):
        """Test creating a comment for authenticated users."""
        post = Post.objects.create(author=self.user,description='sample des')
        payload = {
           
            'comment':'hi',
        }
        url = detail_url(post.id)
        response  = self.client.post(url, payload)
        
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['comment'], payload['comment'])
   
    def test_retrive_comments(self):
        """Test for retrieving a comment."""
        post = Post.objects.create(author=self.user,description='sample')
        comment = Comment.objects.create(post=post,author=self.user,comment='bla')

        url = manage_comment(comment.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['comment'], comment.comment)
    
    def test_patch_comment(self):
        """Test patch a comment."""
        post = Post.objects.create(author=self.user,description='sample')
        comment = Comment.objects.create(post=post,author=self.user,comment='bla')
        payload = {
            'comment':'patch comment'
        }
        url = manage_comment(comment.id)
        response = self.client.patch(url,payload)
        comment.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(comment.comment, payload['comment'])

    def test_all_update(self):
        """Test all update for a comment."""
        post = Post.objects.create(author=self.user,description='sample')
        comment = Comment.objects.create(post=post,author=self.user,comment='bla')
        payload = {
            'post':post,
            'author':self.user,
            'comment':'updated comments'
        }
        url = manage_comment(comment.id)
        response = self.client.put(url, payload)
        comment.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(comment.comment, payload['comment'])

    def test_delete_comment(self):
        """Test delete a comment."""
        post = Post.objects.create(author=self.user,description='sample')
        comment = Comment.objects.create(post=post,author=self.user,comment='bla')
        url = manage_comment(comment.id)
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())