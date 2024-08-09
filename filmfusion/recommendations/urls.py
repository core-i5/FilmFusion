from django.urls import path
from .views import (
    FetchMovieData, RecommendationAPIView,
    GenreMoviesView, MovieDetailView,
    MovieListView, ElasticsearchSearchView
)

urlpatterns = [
    path('fetch/', FetchMovieData.as_view(), name='fetch'),
    path('recommendations/', RecommendationAPIView.as_view(), name='recommendations'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('search/', ElasticsearchSearchView.as_view(), name='search'),
    path('genres/<int:pk>/movies/', GenreMoviesView.as_view(), name='genre-movies'),
    path('movies/', MovieListView.as_view(), name='movie-list'),

]