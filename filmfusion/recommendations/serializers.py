from rest_framework import serializers
from .models import Movie, Genre
from reviews.models import Review
from reviews.pagination import ReviewPagination
from reviews.serializers import ReviewSerializer
from .pagination import MoviePagination

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True) 

    class Meta:
        model = Movie
        fields = [
            'id','tmdb_id', 'imdb_id', 'title', 'tagline', 'overview', 'release_date', 'popularity', 'vote_average', 'vote_count', 'poster_path', 'genres'
        ]

    def create(self, validated_data):
        genres_data = validated_data.pop('genres')
        movie = Movie.objects.create(**validated_data)
        
        # Create or get the genres and associate them with the movie
        for genre_data in genres_data:
            genre, created = Genre.objects.get_or_create(name=genre_data['name'])
            movie.genres.add(genre)

        return movie
    
class MovieListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    class Meta:
        model = Movie
        fields = [
            'id', 'tmdb_id', 'imdb_id', 'title', 'tagline', 'overview', 'release_date', 'popularity', 'vote_average', 'vote_count', 'poster_path','genres'
        ]

class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 'tmdb_id', 'imdb_id', 'title', 'tagline', 'overview', 'release_date', 'popularity', 'vote_average', 'vote_count', 'poster_path', 'genres', 'reviews'
        ]
    
    def get_reviews(self, movie):
        reviews = Review.objects.filter(movie=movie).order_by('created_at') 
        paginator = ReviewPagination()
        paginated_reviews = paginator.paginate_queryset(reviews, self.context['request'])
        serializer = ReviewSerializer(paginated_reviews, many=True, context=self.context)
        return paginator.get_paginated_response(serializer.data).data


class GenreMoviesSerializer(serializers.ModelSerializer):
    movies = serializers.SerializerMethodField()
    
    class Meta:
        model = Genre
        fields = ['name', 'movies']
    
    
    def get_movies(self, genre):
        movies = genre.movie_set.all().order_by('title')
        paginator = MoviePagination()
        paginated_movies = paginator.paginate_queryset(movies, self.context['request'])
        serializer = MovieListSerializer(paginated_movies, many=True)
        return paginator.get_paginated_response(serializer.data).data
    