from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Movie
from reviews.models import Review
from .search_indexes import MovieDocument, ReviewDocument

@receiver(post_save, sender=Movie)
def update_movie_index(sender, instance, **kwargs):
    MovieDocument().update(instance)

@receiver(post_delete, sender=Movie)
def delete_movie_index(sender, instance, **kwargs):
    MovieDocument().delete(instance)

@receiver(post_save, sender=Review)
def update_review_index(sender, instance, **kwargs):
    ReviewDocument().update(instance)

@receiver(post_delete, sender=Review)
def delete_review_index(sender, instance, **kwargs):
    ReviewDocument().delete(instance)
