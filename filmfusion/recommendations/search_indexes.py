# from django_elasticsearch_dsl import Document, fields
# from django_elasticsearch_dsl.registries import registry
# from .models import Movie
# from reviews.models import Review

# @registry.register_document
# class MovieDocument(Document):
#     genres = fields.ObjectField(properties={
#         'name': fields.TextField()
#     })
    
#     class Index:
#         name = 'movies'

#     class Django:
#         model = Movie
#         fields = [
#             'tmdb_id', 'imdb_id', 'title', 'tagline', 'overview', 
#             'release_date', 'popularity', 'vote_average', 'vote_count', 
#             'poster_path'
#         ]

# @registry.register_document
# class ReviewDocument(Document):
#     movie = fields.ObjectField(properties={
#         'title': fields.TextField()
#     })
    
#     class Index:
#         name = 'reviews'

#     class Django:
#         model = Review
#         fields = [
#             'content', 'rating', 'created_at', 'updated_at'
#         ]
