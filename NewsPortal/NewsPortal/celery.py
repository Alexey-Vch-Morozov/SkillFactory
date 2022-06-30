import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')
app = Celery('NewsPortal')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
# Запуск через: celery -A NewsPortal worker -l INFO -P eventlet


app.conf.beat_schedule = {
    'action_send_mail': {
        'task': 'tasks.send_email_weekly',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}
