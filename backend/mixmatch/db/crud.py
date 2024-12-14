from cachetools import cached, TTLCache
from datetime import datetime, timedelta
from fastapi_pagination.ext.sqlalchemy import paginate
from itertools import chain
from sqlalchemy.sql.expression import func
from sqlmodel import Session, and_, or_, select

from mixmatch.db.database import get_db
from mixmatch.db.filters.sorting import music_sort, playlist_sort
from mixmatch.db.functions import unaccent
from mixmatch.db.models import Genre, Music, MusicSearchQuery, Playlist, PlaylistItem, PlaylistSearchQuery
from mixmatch.db.models import Task, TaskResult, User, UserSession
from mixmatch.core.utils import get_compatible_keys


def get_genre(db: Session, genre_id: int):
    return db.get(Genre, genre_id)


def get_genre_by_name(db: Session, genre_name: str):
    statement = select(Genre).where(Genre.name == genre_name)
    return db.exec(statement).first()


def get_genres(db: Session):
    statement = select(Genre).order_by(Genre.name)
    return db.exec(statement).all()


def create_genre(db: Session, genre: Genre):
    db.add(genre)
    db.commit()
    db.refresh(genre)
    return genre


def get_or_create_genre(db: Session, genre: Genre):
    db_genre = get_genre_by_name(db=db, genre_name=genre.name)
    if db_genre:
        return db_genre
    else:
        return create_genre(db=db, genre=genre)


def remove_genre(db: Session, genre: Genre):
    db.delete(genre)
    db.commit()


def get_music_item(db: Session, music_id: int):
    return db.get(Music, music_id)


def get_music_item_by_path(db: Session, path: str):
    statement = select(Music).where(Music.path == path)
    return db.exec(statement).first()


def get_music_items(db: Session):
    statement = select(Music).order_by(Music.artist).order_by(Music.title)
    return db.exec(statement).all()


def get_music_items_paginated(db: Session):
    statement = select(Music).order_by(Music.artist).order_by(Music.title)
    return paginate(db, statement)


def search_music_items_paginated(db: Session, music_search_query: MusicSearchQuery):
    statement = select(Music)
    if music_search_query.artist:
        statement = statement.filter(unaccent(Music.artist).icontains(music_search_query.artist))
    if music_search_query.title:
        statement = statement.filter(unaccent(Music.title).icontains(music_search_query.title))
    if music_search_query.genre_id:
        statement = statement.where(Music.genre_id == music_search_query.genre_id)
    if music_search_query.year_lowest and music_search_query.year_highest:
        statement = statement.where(Music.date >= music_search_query.year_lowest)
        statement = statement.where(Music.date <= music_search_query.year_highest)
    if music_search_query.bpm_lowest and music_search_query.bpm_highest:
        statement = statement.where(Music.bpm >= music_search_query.bpm_lowest)
        statement = statement.where(Music.bpm <= music_search_query.bpm_highest)
    if music_search_query.key:
        if music_search_query.include_compatible_keys:
            compatible_keys = [get_compatible_keys(k, True) for k in music_search_query.key]
            statement = statement.filter(Music.key.in_(list(chain.from_iterable(compatible_keys))))
        else:
            statement = statement.filter(Music.key.in_(music_search_query.key))
    if music_search_query.rating_lowest and music_search_query.rating_highest:
        statement = statement.where(Music.rating >= music_search_query.rating_lowest)
        statement = statement.where(Music.rating <= music_search_query.rating_highest)
    if music_search_query.sort_by:
        statement = music_sort(statement, music_search_query.sort_by, music_search_query.sort_order)
    if music_search_query.random:
        statement = statement.order_by(func.random())
    else:
        statement = statement.order_by(Music.artist).order_by(Music.title)
    return paginate(db, statement)


def create_music_item(db: Session, music_item: Music):
    db.add(music_item)
    db.commit()
    db.refresh(music_item)
    return music_item


def remove_music_item(db: Session, music_item: Music):
    db.delete(music_item)
    db.commit()


def update_music_item(db: Session, music_item: Music, music_item_data: dict[str, any]):
    music_item.sqlmodel_update(music_item_data)
    music_item.genre = music_item_data.get('genre')
    db.add(music_item)
    db.commit()
    db.refresh(music_item)
    return music_item


def create_playlist(db: Session, playlist: Playlist, owner: User):
    playlist.owner = owner
    db.add(playlist)
    db.commit()
    db.refresh(playlist)
    return playlist


def remove_playlist(db: Session, playlist: Playlist):
    db.delete(playlist)
    db.commit()


def get_playlist(db: Session, playlist_id: int, owner: User):
    statement = select(Playlist).where(Playlist.owner == owner).where(Playlist.id == playlist_id)
    return db.exec(statement).first()


def get_playlists_paginated(db: Session, owner: User):
    statement = select(Playlist).where(Playlist.owner == owner).order_by(Playlist.name)
    return paginate(db, statement)


def search_playlists_paginated(db: Session, owner: User, playlist_search_query: PlaylistSearchQuery):
    statement = select(Playlist).where(Playlist.owner == owner)
    if playlist_search_query.name:
        statement = statement.filter(Playlist.name.icontains(playlist_search_query.name))
    if playlist_search_query.sort_by:
        statement = playlist_sort(statement, playlist_search_query.sort_by, playlist_search_query.sort_order)
    statement = statement.order_by(Playlist.name)
    return paginate(db, statement)


def update_playlist(db: Session, playlist: Playlist, playlist_data: dict[str, any]):
    playlist.sqlmodel_update(playlist_data)
    db.add(playlist)
    db.commit()
    db.refresh(playlist)
    return playlist


def get_playlist_item(db: Session, playlist_item_id: int):
    return db.get(PlaylistItem, playlist_item_id)


def create_playlist_item(db: Session, playlist_item: PlaylistItem):
    db.add(playlist_item)
    db.commit()
    db.refresh(playlist_item)
    return playlist_item


def remove_playlist_item(db: Session, playlist_item: PlaylistItem):
    db.delete(playlist_item)
    db.commit()


def update_playlist_item(db: Session, playlist_item: PlaylistItem, playlist_item_data: dict[str, any]):
    playlist_item.sqlmodel_update(playlist_item_data)
    db.add(playlist_item)
    db.commit()
    db.refresh(playlist_item)
    return playlist_item


def get_tasks(db: Session):
    statement = select(Task).order_by(Task.id)
    return db.exec(statement).all()


def get_tasks_running(db: Session):
    statement = select(TaskResult)
    statement = statement.where(or_(TaskResult.completed >= datetime.now() - timedelta(minutes=5),
                                    TaskResult.state.in_(['PENDING', 'RECEIVED', 'RETRY', 'STARTED'])))
    return db.exec(statement).all()


def get_task(db: Session, task_id: str):
    return db.get(Task, task_id)


def get_task_result(db: Session, task_result_id: str):
    return db.get(TaskResult, task_result_id)


def get_task_results_older_than_days(db: Session, days: int):
    statement = select(TaskResult).where(TaskResult.completed <= datetime.now() - timedelta(days=days))
    return db.exec(statement).all()


def create_task_result(db: Session, task_result: TaskResult):
    db.add(task_result)
    db.commit()
    db.refresh(task_result)
    return task_result


def update_task_result(db: Session, task_result: TaskResult, task_result_data: dict[str, any]):
    task_result.sqlmodel_update(task_result_data)
    db.add(task_result)
    db.commit()
    db.refresh(task_result)
    return task_result


def update_task_results_stale(db: Session):
    statement = select(TaskResult).where(and_(TaskResult.started <= datetime.now() - timedelta(days=1),
                                              TaskResult.state.notin_(['FAILURE', 'REVOKED', 'SUCCESS'])))
    task_results = db.exec(statement).all()
    for task_result in task_results:
        task_result.state = 'TIMEOUT'
        db.add(task_result)
        db.commit()
        db.refresh(task_result)
    return task_results


def remove_task_result(db: Session, task_result: TaskResult):
    db.delete(task_result)
    db.commit()


def get_user(db: Session, username: str):
    return db.get(User, username)


def get_users(db: Session):
    statement = select(User).order_by(User.username)
    return db.exec(statement).all()


def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def remove_user(db: Session, user: User):
    db.delete(user)
    db.commit()


def update_user(db: Session, user: User, user_data: dict[str, any]):
    user.sqlmodel_update(user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_password(db: Session, db_user: User, hashed_password: str):
    db_user.password = hashed_password
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_session(db: Session, session_token: str):
    return db.get(UserSession, session_token)


@cached(TTLCache(maxsize=1024, ttl=30))
def get_user_session_cached(session_token: str):
    return get_user_session(db=next(get_db()), session_token=session_token)


def get_user_sessions_expired(db: Session):
    statement = select(UserSession).where(func.current_timestamp() > UserSession.expires)
    return db.exec(statement).all()


def create_user_session(db: Session, user_session: UserSession):
    db.add(user_session)
    db.commit()
    db.refresh(user_session)
    return user_session


def remove_user_session(db: Session, session_token: str):
    user_session = db.get(UserSession, session_token)
    if user_session:
        db.delete(user_session)
        db.commit()
