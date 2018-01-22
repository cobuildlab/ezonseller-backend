from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from django.utils import timezone

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ezonseller.settings')
app = Celery('ezonseller')
# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

#encender worker
# celery -A ezonseller worker -l info

#encender celery beat
# celery -A ezonseller beat -l info -S django

#Cerrar worker
#pkill -9 -f 'celery worker'