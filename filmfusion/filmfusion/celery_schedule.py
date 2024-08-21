from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'fetch-movies-every-30-days': {
        'task': 'recommendations.tasks.fetch_and_store_movies',
        'schedule': crontab(day_of_month='1', hour=0, minute=0),  
    },
}
