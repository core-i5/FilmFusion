import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Movie, Genre
from .serializers import MovieSerializer
from django.apps import apps

RecommendationsConfig = apps.get_app_config('recommendations')

class FetchMovieData(APIView):
    api_key = settings.TMDB_API_KEY
    access_token = settings.TMDB_ACCESS_TOKEN    

    def fetch_movie_data(self, movie_id):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={self.api_key}"
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        response = requests.get(url, headers=headers)
        return response

    def process_movie_data(self, data):
        genres = data.get('genres', [])
        genre_instances = []

        for genre in genres:
            genre_instance, created = Genre.objects.get_or_create(name=genre['name'])
            genre_instances.append(genre_instance)

        poster_path = data.get('poster_path') or data.get('backdrop_path')
        full_poster_path = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None


        movie_data = {
            'tmdb_id': data.get('id'),
            'imdb_id': data.get('imdb_id'),
            'title': data.get('original_title'),
            'tagline': data.get('tagline'),
            'overview': data.get('overview'),
            'release_date': data.get('release_date'),
            'popularity': data.get('popularity'),
            'vote_average': data.get('vote_average'),
            'vote_count': data.get('vote_count'),
            'poster_path': full_poster_path,
            'genres': [{'name': genre.name} for genre in genre_instances]
        }

        serializer = MovieSerializer(data=movie_data)
        if serializer.is_valid():
            movie = serializer.save()
            movie.genres.set(genre_instances)
            return serializer.data, None
        else:
            return None, serializer.errors

    def post(self, request):
        movie_ids = request.data.get('movie_id', [])
        results = []

        for movie_id in movie_ids:
            try:
                if Movie.objects.filter(tmdb_id=movie_id).exists():
                    movie = Movie.objects.get(tmdb_id=movie_id)
                    movie_data = MovieSerializer(movie).data
                    results.append(movie_data)
                else:
                    response = self.fetch_movie_data(movie_id)
                    
                    if response.status_code == 200:
                        data = response.json()
                        movie_data, errors = self.process_movie_data(data)
                        if movie_data:
                            results.append(movie_data)
                        else:
                            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        results.append(None)
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
        return Response(results, status=status.HTTP_200_OK)


data = RecommendationsConfig.data
cosine_sim = RecommendationsConfig.cosine_sim
predicted_ratings_df = RecommendationsConfig.predicted_ratings_df

class RecommendationAPIView(APIView):
    def get(self, request):
        try:
            user_id = None
            movie_id = None
            if "user_id" in request.query_params:
                user_id = int(request.query_params.get('user_id'))
            if "movie_id" in request.query_params:
                movie_id = int(request.query_params.get('movie_id'))
            num_recommendations = int(request.query_params.get('num_recommendations', 10))

            recommendations = hybrid_recommendations(user_id=user_id, movie_id=movie_id, num_recommendations=num_recommendations)
            return Response(recommendations, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
       

def get_content_recommendations(movie_id, num_recommendations=10):
    movie_idx = data[data['id'] == movie_id].index[0]
    sim_scores = list(enumerate(cosine_sim[movie_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations+1]
    movie_indices = [i[0] for i in sim_scores]
    return [(int(data['id'].iloc[idx]), data['title'].iloc[idx]) for idx in movie_indices]

def get_popularity_recommendations(num_recommendations=10):
    popular_movies = data.sort_values('popularity', ascending=False)
    movie_indices = popular_movies.index[:num_recommendations]
    return [(int(data['id'].iloc[idx]), data['title'].iloc[idx]) for idx in movie_indices]

def hybrid_recommendations(user_id=None, movie_id=None, num_recommendations=10):
    if user_id is None or user_id not in predicted_ratings_df.index:
        if movie_id is not None:
            return get_content_recommendations(movie_id, num_recommendations)
        else:
            return get_popularity_recommendations(num_recommendations)
    else:
        user_ratings = predicted_ratings_df.loc[user_id]
        cf_recommendations = user_ratings.sort_values(ascending=False).index[:num_recommendations]

        if movie_id is not None:
            content_recommendations = get_content_recommendations(movie_id, num_recommendations)
            combined_recommendations = list(set(cf_recommendations).union(set([idx for idx, title in content_recommendations])))
            combined_scores = {}

            movie_idx = data[data['id'] == movie_id].index[0]
            for idx in combined_recommendations:
                cf_score = user_ratings.get(idx, 0)
                content_score = cosine_sim[movie_idx][idx] if idx < len(cosine_sim) else 0
                combined_scores[idx] = (cf_score + content_score) / 2

            sorted_recommendations = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:num_recommendations]
            return [(int(data['id'].iloc[idx]), data['title'].iloc[idx]) for idx, score in sorted_recommendations]
        else:
            return [(int(data['id'].iloc[idx]), data['title'].iloc[idx]) for idx in cf_recommendations]
