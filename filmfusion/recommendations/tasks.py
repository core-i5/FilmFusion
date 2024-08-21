from celery import shared_task
import requests
from .models import Movie, Genre, TaskState
from .serializers import MovieSerializer
from django.conf import settings
import logging
import time

logger = logging.getLogger('celery')

@shared_task
def fetch_and_store_movies():
    api_key = settings.TMDB_API_KEY
    access_token = settings.TMDB_ACCESS_TOKEN

    def fetch_movie_data(movie_id):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        return response

    def process_movie_data(data):
        genres = data.get('genres', [])
        genre_instances = []

        for genre in genres:
            genre_instance, _ = Genre.objects.get_or_create(name=genre['name'])
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
            return True
        else:
            logger.error(f"Serializer errors: {serializer.errors}")
            return False

    # Get or create the task state
    task_state, _ = TaskState.objects.get_or_create(task_name='fetch_and_store_movies')

    # Fetch the latest movie ID from TMDB
    url = f"https://api.themoviedb.org/3/movie/latest?api_key={api_key}"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error("Failed to fetch the latest movie ID")
        return
    latest_movie_id = response.json().get('id', 0)

    current_movie_id = task_state.last_processed_movie_id + 1  # Start from the last processed movie ID

    while current_movie_id <= latest_movie_id:
        try:
            if Movie.objects.filter(tmdb_id=current_movie_id).exists():
                logger.info(f"Movie with ID {current_movie_id} already exists in the database.")
            else:
                response = fetch_movie_data(current_movie_id)
                if response.status_code == 200:
                    process_movie_data(response.json())
                else:
                    logger.error(f"Failed to fetch movie with ID {current_movie_id}")
                    task_state.failed_movie_ids.append(current_movie_id)  # Track failed movie IDs
            time.sleep(0.25)  # 250ms delay to stay within rate limit (40 requests per 10 seconds)
        except Exception as e:
            logger.exception(f"Error processing movie ID {current_movie_id}: {str(e)}")

        task_state.last_processed_movie_id = current_movie_id
        task_state.save()  # Save progress after each movie
        current_movie_id += 1
