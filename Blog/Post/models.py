from django.db import models
from django.contrib.auth.models import User


class BlogPost(models.Model):
    title = models.CharField(max_length=50)
    post = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default=None)
    updated_date = models.DateTimeField(auto_now=True)


class BlogComments(models.Model):
    comment = models.CharField(max_length=100)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

# migration issues --> https://docs.djangoproject.com/en/dev/ref/django-admin/#migrate

