from __future__ import absolute_import
import os
from celery import Celery
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pub_g.settings')
django.setup()
app = Celery('pub_g')
app.config_from_object('django.conf:settings')

# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
