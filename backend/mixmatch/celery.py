from celery import Celery
from celery.schedules import crontab
from mixmatch import __application__
from mixmatch.core.settings import settings


celery = Celery(
    __application__,
    broker=str(settings.celery_broker_dsn),
    backend="rpc://",
    broker_connection_retry_on_startup=True,
    include=['mixmatch.tasks']
)

celery.conf.beat_schedule = {
    'task_cleanup': {
        'task': 'mixmatch.tasks.tasks.task_cleanup',
        'schedule': crontab(minute='0', hour='0', day_of_month='1')
    },
    'task_import': {
        'task': 'mixmatch.tasks.tasks.task_import',
        'schedule': crontab(minute='0')
    }
}
