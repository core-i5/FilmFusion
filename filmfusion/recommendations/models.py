from django.db import models
from users.models import UUIDModel

class Genre(UUIDModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(UUIDModel):
    tmdb_id = models.IntegerField(unique=True)
    imdb_id = models.CharField(max_length=15, null=True, blank=True)
    title = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255, null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    poster_path = models.URLField(null=True, blank=True)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title

class TaskState(models.Model):
    task_name = models.CharField(max_length=255)
    last_processed_movie_id = models.IntegerField(default=0)
    failed_movie_ids = models.JSONField(default=list)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)