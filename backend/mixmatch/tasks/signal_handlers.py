from celery import states
from celery.signals import before_task_publish, task_postrun, task_prerun
from datetime import datetime
from json import dumps
from mixmatch.db import crud
from mixmatch.db.database import get_db
from mixmatch.db.models import TaskResult

TASK_PREFIX = 'mixmatch.tasks.tasks.task_'


@before_task_publish.connect()
def before_task_publish_handler(headers=None, **kwargs):
    if headers.get('task').startswith(TASK_PREFIX):
        task_result = TaskResult(id=headers.get('id'), task_id=headers.get('task'), state=states.PENDING)
        crud.create_task_result(db=next(get_db()), task_result=task_result)


@task_prerun.connect()
def task_prerun_handler(task_id=None, task=None, **kwargs):
    db = next(get_db())
    if task.name.startswith(TASK_PREFIX):
        task_result = TaskResult(id=task_id, task_id=task.name, state=states.STARTED, started=datetime.now())
        db_task_result = crud.get_task_result(db=db, task_result_id=task_id)
        crud.update_task_result(db=db, task_result=db_task_result,
                                task_result_data=task_result.model_dump(exclude_unset=True))


@task_postrun.connect()
def task_postrun_handler(task_id=None, task=None, retval=None, state=None, **kwargs):
    db = next(get_db())
    if task.name.startswith(TASK_PREFIX):
        task_result = TaskResult(id=task_id, task_id=task.name, state=state,
                                 result=dumps(retval), completed=datetime.now())
        db_task_result = crud.get_task_result(db=db, task_result_id=task_id)
        crud.update_task_result(db=db, task_result=db_task_result,
                                task_result_data=task_result.model_dump(exclude_unset=True))
