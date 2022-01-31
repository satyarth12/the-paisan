from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
# from celery.schedules import crontab  ## for allocating a periodic task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bingeman_backend.settings')

app = Celery('bingeman_backend')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
