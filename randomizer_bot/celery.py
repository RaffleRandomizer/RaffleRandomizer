import os
from datetime import timedelta
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'randomizer_bot.settings')
app = Celery('randomizer_bot')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()
