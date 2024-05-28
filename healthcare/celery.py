from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab # type: ignore

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare.settings')

app = Celery('healthcare')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-appointments-every-minute': {
        'task': 'api.tasks.check_appointments',  # the name of the task
        'schedule': 60.0,  # run every 60 seconds
    },
}