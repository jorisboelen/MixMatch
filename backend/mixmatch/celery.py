from celery import Celery
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
        'schedule': settings.TASK_CLEANUP_CRON
    },
    'task_import': {
        'task': 'mixmatch.tasks.tasks.task_import',
        'schedule': settings.TASK_IMPORT_CRON
    }
}
