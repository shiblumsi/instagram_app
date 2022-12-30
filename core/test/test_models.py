from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from unittest.mock import patch 



def create_user(email='abc@abc.com', password='testpass'):
    return get_user_model().objects.create_user(email,password)


class ModelTests(TestCase):
    def test_ctrate_user_with_email_successful(self):
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password = password
        )
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raise_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser('test@example.com','test123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_post_app(self):
        user = create_user()

        post = models.Post.objects.create(
            author = user,
            photo = 'ggg.jpg', 
            description = 'djaklfja'      
        )
        self.assertEqual(str(post), post.description)

    def test_create_comment(self):
        user = create_user()
        post = models.Post.objects.create(author=user,photo='gg.jpg')
        comment = models.Comment.objects.create(author=user,post=post,comment='comments')
        self.assertEqual(str(comment), comment.comment)

