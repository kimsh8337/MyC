from django.db import models
from django.conf import settings
from movies.models import Movie

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    title = models.CharField(max_length=30)
    score = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_posts")

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)