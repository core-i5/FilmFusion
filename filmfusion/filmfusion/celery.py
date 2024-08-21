from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import logging

logger = logging.getLogger('django')


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'filmfusion.settings')

app = Celery('filmfusion')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# Load the schedule from the separate file
try:
    from .celery_schedule import CELERY_BEAT_SCHEDULE
    app.conf.update(beat_schedule=CELERY_BEAT_SCHEDULE)
except Exception as e:
    logger.exception(f"Failed to import or apply CELERY_BEAT_SCHEDULE: {str(e)}")