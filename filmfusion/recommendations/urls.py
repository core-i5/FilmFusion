from django.urls import path
from .views import (
    FetchMovieData, RecommendationAPIView,
    GenreMoviesView, MovieDetailView,
    MovieListView, 
    # ElasticsearchSearchView
)

urlpatterns = [
    path('fetch/', FetchMovieData.as_view(), name='fetch'),
    path('recommendations/', RecommendationAPIView.as_view(), name='recommendations'),
    path('<uuid:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    # path('search/', ElasticsearchSearchView.as_view(), name='search'),
    path('genres/<uuid:pk>/', GenreMoviesView.as_view(), name='genre-movies'),
    path('', MovieListView.as_view(), name='movie-list'),

]