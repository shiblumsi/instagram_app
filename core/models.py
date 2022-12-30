from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models
import uuid
import os
from django.conf import settings


def post_image_file_path(instance, filename):
    """Generate file path for new post image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'post', filename)

User = settings.AUTH_USER_MODEL

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('user must have email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    def __str__(self):
        return self.name




class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_posts')
    photo = models.ImageField(upload_to=post_image_file_path,blank=True,editable=False,null=True)
    description = models.TextField(blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name='likers',blank=True, symmetrical=False)

    

    def number_of_likes(self):
        if self.likes.count():
            return self.likes.count()
        else:
            return 0

    def __str__(self):
        return str(self.description) 



class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_comments')
    author = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='user_comments',null=True,blank=True)
    comment = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.comment}'