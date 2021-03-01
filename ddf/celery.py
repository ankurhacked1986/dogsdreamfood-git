import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE','ddf.settings')
app = Celery('ddf')
app.config_from_object('django.conf:settings',namespace = 'CELERY')
app.autodiscover_tasks()