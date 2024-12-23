from argon2 import PasswordHasher
from datetime import datetime, timedelta
from faker import Faker
from faker.providers import address, date_time
from mixmatch.core.settings import settings
from mixmatch.core.utils import get_compatible_keys
from mixmatch.db import crud
from mixmatch.db.database import get_db
from mixmatch.db.models import Music, Playlist, User, UserSession
from random import choice
from secrets import token_hex

fake = Faker()
fake.add_provider(address)
fake.add_provider(date_time)


def generate_user_token(username: str, save_to_db: bool=True):
    token = UserSession(token=token_hex(), username=username,
                        expires=datetime.now() + timedelta(seconds=settings.SESSION_EXPIRE_SECONDS))
    if save_to_db:
        crud.create_user_session(db=next(get_db()), user_session=token)
    return token


def generate_music_search_queries_matching(music_item: Music):
    # empty query
    q1 = [{}]
    # single field, exact match
    q2 = [{'artist': music_item.artist}, {'title': music_item.title}, {'genre_id': music_item.genre.id},
          {'year_lowest': music_item.date, 'year_highest': music_item.date},
          {'bpm_lowest': music_item.bpm, 'bpm_highest': music_item.bpm}, {'key': [music_item.key]},
          {'rating_lowest': music_item.rating, 'rating_highest': music_item.rating}]
    # single field, partial match
    q3 = [{'artist': music_item.artist[fake.random_int(min=0, max=2):fake.random_int(min=-5, max=0)]},
          {'title': music_item.title[fake.random_int(min=0, max=2):fake.random_int(min=-5, max=0)]},
          {'year_lowest': str(int(music_item.date) - fake.random_int(min=0, max=50)),
           'year_hightest': str(int(music_item.date) + fake.random_int(min=0, max=50))},
          {'bpm_lowest': music_item.bpm - fake.random_int(min=0, max=20),
           'bpm_hightest': music_item.bpm + fake.random_int(min=0, max=20)},
          {'key': [choice(get_compatible_keys(music_item.key))], 'include_compatible_keys': True},
          {'key': get_compatible_keys(music_item.key), 'include_compatible_keys': True},
          {'rating_lowest': fake.random_int(min=0, max=music_item.rating),
           'rating_highest': fake.random_int(min=music_item.rating, max=5)}]
    # multiple fields
    q4 = [{**choice(q2 + q3), **choice(q2 + q3)} for _ in range(1,10)]
    # combine all queries
    return q1 + q2 + q3 + q4


def generate_playlist_search_queries_matching(playlist: Playlist):
    # empty query
    q1 = [{}]
    # single field, exact match
    q2 = [{'name': playlist.name}]
    # single field, partial match
    q3 = [{'name': playlist.name[fake.random_int(min=0, max=2):fake.random_int(min=-5, max=0)]}]
    # combine all queries
    return q1 + q2 + q3


def get_or_create_user(username: str, password: str, is_admin: bool, db=next(get_db())):
    user = crud.get_user(db=db, username=username)
    if not user:
        return crud.create_user(db=db, user=User(username=username,
                                                 password=PasswordHasher().hash(password),
                                                 is_admin=is_admin))
    else:
        return user
