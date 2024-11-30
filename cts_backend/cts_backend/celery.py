from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Configuración básica de Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cts_backend.settings')
app = Celery('cts_backend')

# Cargar la configuración desde Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubrir tareas de todas las apps registradas
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
