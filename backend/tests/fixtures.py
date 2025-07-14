import pytest
import mixmatch
from alembic.command import upgrade
from alembic.config import Config
from mixmatch.core.settings import settings
from mixmatch.db import crud
from mixmatch.db.database import get_db
from mixmatch.db.models import Genre, GenreCreate, Playlist, PlaylistCreate, PlaylistItem, PlaylistItemCreate, Track
from mixmatch.db.models import User, UserCreate
from mixmatch.file import mixmatch_file
from mixmatch.tasks.utils import save_cover
from os.path import dirname, join
from pathlib import Path
from random import choice
from shutil import copy
from uuid import uuid4
from .utils import fake, generate_user_token, get_or_create_user

RESOURCES_PATH = join(dirname(__file__), "resources")
RESOURCES_COVER = [p for p in Path(join(RESOURCES_PATH, 'cover')).rglob('*.jpg') if p.is_file()]
RESOURCES_TRACK = [p for p in Path(join(RESOURCES_PATH, 'track')).rglob('*.mp3') if p.is_file()]
RESOURCES_GENRE = open(join(RESOURCES_PATH, 'genres.txt'), 'r').read().splitlines()  # www.musicgenreslist.com

USER_ADMIN_USERNAME = fake.user_name()
USER_ADMIN_PASSWORD = fake.password(length=fake.random_int(min=8, max=32))
USER_VIEWER_USERNAME = fake.user_name()
USER_VIEWER_PASSWORD = fake.password(length=fake.random_int(min=8, max=32))


@pytest.fixture(autouse=True)
def alembic_upgrade():
    config = Config(file_=join(dirname(mixmatch.__file__), "alembic.ini"))
    config.set_main_option("script_location", join(dirname(mixmatch.__file__), "alembic"))
    upgrade(config, "head")


@pytest.fixture()
def genre(db=next(get_db())):
    return crud.get_or_create_genre(db=db, genre=Genre(name=choice(RESOURCES_GENRE)))


@pytest.fixture()
def genre_create():
    return GenreCreate(name=choice(RESOURCES_GENRE))


@pytest.fixture()
def track(db=next(get_db())):
    test_track_resource = choice(RESOURCES_TRACK)
    test_track_path = join(settings.MUSIC_DIRECTORY, f'{str(uuid4())}{test_track_resource.suffix}')
    copy(test_track_resource, test_track_path)
    test_music_file = mixmatch_file(Path(test_track_path))
    test_music_file.artist = fake.name()
    test_music_file.title = fake.city()
    test_music_file.album = fake.country()
    test_music_file.genre = choice(RESOURCES_GENRE)
    test_music_file.date = fake.date_object()
    test_music_file.save()
    test_track = Track(**test_music_file.model_dump(exclude={'cover', 'genre'}))
    test_track.cover = save_cover(test_music_file.cover)
    test_track.genre = crud.get_or_create_genre(db=db, genre=Genre(name=test_music_file.genre))
    test_track.rating = fake.random_int(min=0, max=5)
    return crud.create_track(db=db, track=test_track)


@pytest.fixture()
def track_cover():
    return choice(RESOURCES_COVER)


@pytest.fixture()
def playlist():
    def playlist(owner_username: str, db=next(get_db())):
        owner = crud.get_user(db=db, username=owner_username)
        return crud.create_playlist(db=db, playlist=Playlist(name=fake.country()), owner=owner)
    return playlist


@pytest.fixture()
def playlist_create():
    return PlaylistCreate(name=fake.city())


@pytest.fixture()
def playlist_item(playlist, track):
    def playlist_item(owner_username: str, playlist=playlist, track=track, db=next(get_db())):
        user_playlist = playlist(db=db, owner_username=owner_username)
        return crud.create_playlist_item(db=db, playlist_item=PlaylistItem(playlist=user_playlist,
                                                                           track=db.merge(track),
                                                                           order=fake.random_int(min=0, max=99)))
    return playlist_item


@pytest.fixture()
def playlist_item_create(playlist, track):
    def playlist_item_create(owner_username: str, playlist=playlist, track=track, db=next(get_db())):
        user_playlist = playlist(db=db, owner_username=owner_username)
        return PlaylistItemCreate(playlist_id=user_playlist.id, track_id=track.id,
                                  order=fake.random_int(min=0, max=99))
    return playlist_item_create


@pytest.fixture()
def tasks():
    return [
        {
            'id': 'mixmatch.tasks.tasks.task_cleanup',
            'name': 'Cleanup (covers, user sessions, task results)',
            'results': []
        },
        {
            'id': 'mixmatch.tasks.tasks.task_import',
            'name': 'Perform import of music files',
            'results': []
        }
    ]


@pytest.fixture()
def user():
    return crud.create_user(db=next(get_db()), user=User(username=fake.user_name(), is_admin=choice([True, False]),
                                                         password=fake.password(length=fake.random_int(min=8, max=32))))


@pytest.fixture()
def user_create():
    return UserCreate(username=fake.user_name(), password=fake.password(length=fake.random_int(min=8, max=32)),
                      is_admin=choice([True, False]))


@pytest.fixture()
def users():
    user_admin = get_or_create_user(username=USER_ADMIN_USERNAME, password=USER_ADMIN_PASSWORD, is_admin=True)
    user_viewer = get_or_create_user(username=USER_VIEWER_USERNAME, password=USER_VIEWER_PASSWORD, is_admin=False)

    return {
        'correct': [
            {'username': user_admin.username, 'password': USER_ADMIN_PASSWORD, 'is_admin': True},
            {'username': user_viewer.username, 'password': USER_VIEWER_PASSWORD, 'is_admin': False}
        ],
        'incorrect_password': [
            {'username': user_admin.username, 'password': 'incorrect123'},
            {'username': user_viewer.username, 'password': 'incorrect123'}
        ],
        'incorrect_username': [
            {'username': 'incorrectadmin', 'password': 'incorrect123'},
            {'username': 'incorrectviewer', 'password': USER_VIEWER_PASSWORD}
        ]
    }


@pytest.fixture()
def user_tokens(users):
    return {
        'correct': [generate_user_token(users['correct'][0]['username']),
                    generate_user_token(users['correct'][1]['username'])],
        'incorrect': [generate_user_token(users['correct'][0]['username'], False),
                      generate_user_token(users['correct'][1]['username'], False)]
    }
