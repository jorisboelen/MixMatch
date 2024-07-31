from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlmodel import Session

from mixmatch.api.utils import require_admin_permissions
from mixmatch.db import crud
from mixmatch.db.database import get_db
from mixmatch.db.models import TaskRead, TaskResultWithTaskRead
from mixmatch.tasks import task_cleanup, task_import

router = APIRouter(dependencies=[Depends(require_admin_permissions)])


@router.get("/", response_model=list[TaskRead], status_code=200)
def read_tasks(db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db)
    return tasks


@router.get("/running", response_model=list[TaskResultWithTaskRead], status_code=200)
def read_tasks_running(db: Session = Depends(get_db)):
    tasks = crud.get_tasks_running(db)
    return tasks


@router.get("/{task_id}", response_model=TaskRead, status_code=200)
def read_task(task_id: str, db: Session = Depends(get_db)):
    task = crud.get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/{task_id}/run", status_code=204)
def run_task(task_id: str):
    if task_id == 'mixmatch.tasks.tasks.task_import':
        task_import.delay()
    elif task_id == 'mixmatch.tasks.tasks.task_cleanup':
        task_cleanup.delay()
    else:
        raise HTTPException(status_code=404, detail="Task not found")
