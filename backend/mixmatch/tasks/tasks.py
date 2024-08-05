import logging
import psycopg2.errors
import sqlalchemy.exc
from celery import group
from mixmatch.celery import celery
from mixmatch.core.settings import settings
from mixmatch.db import crud
from mixmatch.db.database import get_db
from mixmatch.db.models import Genre, Music
from mixmatch.file import MusicFile, MixMatchFileError
from os.path import exists
from pathlib import Path
from sqlmodel import Session
from .utils import merge_task_results


@celery.task()
def task_cleanup(path=settings.IMAGE_DIRECTORY, db: Session = next(get_db())):
    logger = logging.getLogger(__name__)
    music_in_db = crud.get_music_items(db)
    covers_in_db = [m.cover for m in music_in_db]
    covers_on_disk = [p for p in Path(path).rglob('*') if p.is_file()]
    result_removed = 0

    for cover in covers_on_disk:
        if cover.name not in covers_in_db:
            logger.info(f"Removing Unused Cover :: {cover.name}")
            result_removed += 1
            cover.unlink()

    return {'removed': result_removed}


@celery.task()
def subtask_import_file(file: str, db: Session = next(get_db())):
    logger = logging.getLogger(__name__)
    logger.info(f'Processing File :: {file}')

    result = {'file': file, 'created': 0, 'updated': 0, 'removed': 0, 'skipped': 0}
    music_item = crud.get_music_item_by_path(db=db, path=file)

    try:
        # process new file
        if not music_item:
            music_file = MusicFile(path=str(file))
            music_file.save_cover()
            music_item = Music(**music_file.to_dict())
            music_item.genre = crud.get_or_create_genre(db=db, genre=Genre(name=music_file.genre))
            crud.create_music_item(db=db, music_item=music_item)
            result['created'] = 1
        # process updated file
        elif int(Path(file).stat().st_mtime) != music_item.mtime:
            music_file = MusicFile(path=str(file))
            music_file.save_cover()
            genre = crud.get_or_create_genre(db=db, genre=Genre(name=music_file.genre))
            crud.update_music_item(db=db, music_item=music_item,
                                   music_item_data={**music_file.to_dict(), **{'genre': genre}})
            result['updated'] = 1
        # proces existing file
        else:
            result['skipped'] = 1
    except MixMatchFileError as e:
        result['skipped'] = 1
        logger.warning(f"[skipping] {str(e)}")
    except (psycopg2.errors.UniqueViolation, sqlalchemy.exc.IntegrityError):
        db.rollback()
        subtask_import_file(file)
    return result


@celery.task()
def task_import(path=settings.MUSIC_DIRECTORY, db: Session = next(get_db())):
    logger = logging.getLogger(__name__)
    logger.info(f'Processing Folder :: {path}')

    music_in_db = crud.get_music_items(db)
    files_on_disk = [str(p) for p in Path(path).rglob('*') if p.is_file()]

    # process files on disk
    workflow = group(subtask_import_file.s(file) for file in files_on_disk)
    workflow_result = workflow.apply_async()
    task_result = merge_task_results(workflow_result.get(disable_sync_subtasks=False))

    # process files in db
    for music_item in music_in_db:
        # process removed file
        if not exists(music_item.path):
            crud.remove_music_item(db=db, music_item=music_item)
            task_result['removed'] += 1

    return task_result
