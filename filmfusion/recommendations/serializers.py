from rest_framework import serializers
from .models import Movie, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True) 

    class Meta:
        model = Movie
        fields = [
            'tmdb_id', 'imdb_id', 'title', 'tagline', 'overview', 'release_date', 'popularity', 'vote_average', 'vote_count', 'poster_path', 'genres'
        ]

    def create(self, validated_data):
        genres_data = validated_data.pop('genres')
        movie = Movie.objects.create(**validated_data)
        
        # Create or get the genres and associate them with the movie
        for genre_data in genres_data:
            genre, created = Genre.objects.get_or_create(name=genre_data['name'])
            movie.genres.add(genre)

        return movie