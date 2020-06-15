from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    release_date = models.DateField(max_length=100)
    popularity = models.FloatField(max_length=100)
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    adult = models.BooleanField()
    overview = models.TextField()
    original_language = models.CharField(max_length=100)
    poster_path = models.TextField(null=True)
    backdrop_path = models.TextField(null=True)

    genre_ids = models.ManyToManyField(Genre, related_name='movie_genres')
    selected_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='selcted_movies')
    watched_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='watched_movies')

    def __str__(self):
        return self.title
    
class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    content = models.CharField(max_length=500)
    standard = models.IntegerField()
    rank = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
