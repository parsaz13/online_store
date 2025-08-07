import os
from celery import Celery

# تنظیم مسیر تنظیمات Django نسبت به ریشه پروژه
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.Config.settings')

app = Celery('backend', broker='amqp://guest:guest@localhost:5672//')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')