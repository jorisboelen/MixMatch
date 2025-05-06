import logging
import psycopg2.errors
import sqlalchemy.exc
from celery import group
from mixmatch.celery import celery
from mixmatch.core.settings import settings
from mixmatch.db import crud
from mixmatch.db.database import get_db
from mixmatch.db.models import Genre, Track
from mixmatch.file import mixmatch_file, MixMatchFileError
from os.path import exists
from pathlib import Path
from sqlmodel import Session
from .utils import merge_task_results, save_cover


def task_cleanup_covers(path=settings.IMAGE_DIRECTORY, db: Session = next(get_db())):
    logger = logging.getLogger(__name__)
    tracks_in_db = crud.get_tracks(db)
    covers_in_db = [m.cover for m in tracks_in_db]
    covers_on_disk = [p for p in Path(path).rglob('*') if p.is_file()]
    result_removed = 0

    for cover in covers_on_disk:
        if cover.name not in covers_in_db:
            logger.info(f"Removing Unused Cover :: {cover.name}")
            result_removed += 1
            cover.unlink()

    return {'covers': result_removed}


def task_cleanup_user_sessions(db: Session = next(get_db())):
    logger = logging.getLogger(__name__)
    expired_user_sessions = crud.get_user_sessions_expired(db)
    result_removed = 0

    for expired_user_session in expired_user_sessions:
        logger.info(f"Removing Expired User Session :: {expired_user_session.token}")
        crud.remove_user_session(db, expired_user_session.token)
        result_removed += 1

    return {'user_sessions': result_removed}


def task_cleanup_task_results(db: Session = next(get_db())):
    logger = logging.getLogger(__name__)
    crud.update_task_results_stale(db)
    expired_task_results = crud.get_task_results_older_than_days(db, 30)
    result_removed = 0

    for expired_task_result in expired_task_results:
        logger.info(f"Removing Task Result :: {expired_task_result.id}")
        crud.remove_task_result(db, expired_task_result)
        result_removed += 1

    return {'task_results': result_removed}


@celery.task()
def task_cleanup():
    result_covers = task_cleanup_covers()
    result_user_sessions = task_cleanup_user_sessions()
    result_task_results = task_cleanup_task_results()
    return {**result_covers, **result_user_sessions, **result_task_results}


@celery.task(bind=True)
def subtask_import_file(self, file: str, db: Session = next(get_db())):
    logger = logging.getLogger(__name__)
    logger.info(f'Processing File :: {file}')

    result = {'file': file, 'created': 0, 'updated': 0, 'removed': 0, 'skipped': 0}
    track = crud.get_track_by_path(db=db, path=file)

    try:
        # process new file
        if not track:
            music_file = mixmatch_file(file_path=Path(file))
            track = Track(**music_file.model_dump(exclude={'cover', 'genre'}))
            track.cover = save_cover(music_file.cover)
            track.genre = crud.get_or_create_genre(db=db, genre=Genre(name=music_file.genre))
            crud.create_track(db=db, track=track)
            result['created'] = 1
        # process updated file
        elif int(Path(file).stat().st_mtime) != track.mtime:
            music_file = mixmatch_file(file_path=Path(file))
            cover = save_cover(music_file.cover)
            genre = crud.get_or_create_genre(db=db, genre=Genre(name=music_file.genre))
            crud.update_track(db=db, track=track,
                              track_data={**music_file.model_dump(exclude={'cover', 'genre'}),
                                          **{'cover': cover, 'genre': genre}})
            result['updated'] = 1
        # proces existing file
        else:
            result['skipped'] = 1
    except MixMatchFileError as e:
        result['skipped'] = 1
        logger.warning(f"[skipping] {str(e)}")
    except (psycopg2.errors.UniqueViolation, sqlalchemy.exc.IntegrityError) as exc:
        db.rollback()
        raise self.retry(exc=exc, countdown=1, max_retries=3)
    except Exception as e:
        result['skipped'] = 1
        logger.error(f'An unexpected error occurred while processing: {file}. Error: {str(e)}')
    return result


@celery.task()
def task_import(path=settings.MUSIC_DIRECTORY, db: Session = next(get_db())):
    logger = logging.getLogger(__name__)
    logger.info(f'Processing Folder :: {path}')

    tracks_in_db = crud.get_tracks(db)
    files_on_disk = [str(p) for p in Path(path).rglob('*') if p.is_file()]

    # process files on disk
    workflow = group(subtask_import_file.s(file) for file in files_on_disk)
    workflow_result = workflow.apply_async()
    task_result = merge_task_results(workflow_result.get(disable_sync_subtasks=False))

    # process files in db
    for track in tracks_in_db:
        # process removed file
        if not exists(track.path):
            crud.remove_track(db=db, track=track)
            task_result['removed'] += 1

    return task_result
