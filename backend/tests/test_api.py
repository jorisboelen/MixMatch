from fastapi.testclient import TestClient
from filecmp import cmp
from mixmatch.app import app
from mixmatch.core.settings import settings
from mixmatch.db.models import Genre, MusicRead, MusicSearchQuery, MusicSearchQuerySortByEnum, SortOrderEnum
from mixmatch.db.models import PlaylistRead, PlaylistItemRead, PlaylistSearchQuery, PlaylistSearchQuerySortByEnum
from mixmatch.db.models import UserBase
from os.path import join
from random import choice
from tempfile import NamedTemporaryFile
from .fixtures import alembic_upgrade, genre, genre_create, music_cover, music_item, playlist, playlist_create
from .fixtures import playlist_item, playlist_item_create, tasks, user_create, user, users, user_tokens
from .utils import fake, generate_music_search_queries_matching, generate_playlist_search_queries_matching

client = TestClient(app)


class TestAnonymous:
    def test_get_docs(self):
        response = client.get("/api/docs")
        assert response.status_code == 200

    def test_get_health(self):
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == {'status': 'ok'}

    def test_post_login_incorrect_password(self, users):
        test_user = choice(users['incorrect_password'])
        response = client.post("/api/login", json=test_user)
        assert response.status_code == 401
        assert response.json() == {'detail': 'Invalid username and/or password'}

    def test_post_login_incorrect_username(self, users):
        test_user = choice(users['incorrect_username'])
        response = client.post("/api/login", json=test_user)
        assert response.status_code == 401
        assert response.json() == {'detail': 'Invalid username and/or password'}

    def test_get_user_me(self):
        response = client.get("/api/user/me")
        assert response.status_code == 403
        assert response.json() == {'detail': 'Not logged in'}


class TestExpired:
    def test_get_users_me(self, user_tokens):
        client.cookies = {'session_token': choice(user_tokens['incorrect']).token}
        response = client.get("/api/users/me")
        assert response.status_code == 403
        assert response.json() == {'detail': 'Session token invalid or expired'}


class TestAdmin:
    def test_post_login(self, users):
        test_user = users['correct'][0]
        response = client.post("/api/login", json=test_user)
        assert response.status_code == 200
        assert response.json().get('username') == test_user['username']

    def test_post_genre(self, genre_create):
        response = client.post("/api/genre/", json=genre_create.model_dump())
        assert response.status_code == 201
        assert response.json().get('name') == genre_create.name

    def test_delete_genre(self, genre):
        response = client.delete(f"/api/genre/{genre.id}")
        assert response.status_code == 204
        response = client.get("/api/genre/")
        assert response.status_code == 200
        assert genre not in [Genre.model_validate(r) for r in response.json()]

    def test_patch_music(self, music_item, genre):
        music_item.artist = fake.country()
        music_item.title = fake.name()
        music_item.album = fake.city()
        music_item.genre_id = genre.id
        music_item.date = fake.year()
        music_item.rating = fake.random_int(min=0, max=5)
        response = client.patch(f"/api/music/{music_item.id}",
                                json={'artist': music_item.artist, 'title': music_item.title,
                                      'album': music_item.album, 'genre_id': music_item.genre_id,
                                      'date': music_item.date, 'rating': music_item.rating})
        assert response.status_code == 200
        assert response.json().get('artist') == music_item.artist
        assert response.json().get('title') == music_item.title
        assert response.json().get('album') == music_item.album
        assert response.json().get('genre').get('id') == music_item.genre_id
        assert response.json().get('date') == music_item.date
        assert response.json().get('rating') == music_item.rating

    def test_delete_music(self, music_item):
        response = client.delete(f"/api/music/{music_item.id}")
        assert response.status_code == 204
        response = client.get("/api/music/", params={'size': 100})
        assert response.status_code == 200
        assert MusicRead.model_validate(music_item) not in [MusicRead.model_validate(r) for r in response.json().get('items')]

    def test_put_music_cover(self, music_item, music_cover):
        response = client.put(f"/api/music/{music_item.id}/cover", files={'music_cover': open(music_cover, 'rb')})
        assert response.status_code == 204
        response = client.get(f"/api/music/{music_item.id}/cover")
        with NamedTemporaryFile(mode='wb') as f:
            f.write(response.content)
            assert response.status_code == 200
            assert cmp(f.name, music_cover)

    def test_get_tasks(self, tasks):
        response = client.get("/api/task/")
        assert response.status_code == 200
        assert response.json() == tasks

    def test_get_tasks_running(self):
        response = client.get("/api/task/running")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_task(self, tasks):
        response = client.get(f"/api/task/{tasks[0].get('id')}")
        assert response.status_code == 200
        assert response.json() == tasks[0]
        response = client.get(f"/api/task/{tasks[1].get('id')}")
        assert response.status_code == 200
        assert response.json() == tasks[1]

    def test_get_users(self, users):
        response = client.get("/api/user/")
        assert response.status_code == 200
        assert UserBase.model_validate(users['correct'][0]) in [UserBase.model_validate(u) for u in response.json()]
        assert UserBase.model_validate(users['correct'][1]) in [UserBase.model_validate(u) for u in response.json()]

    def test_post_user(self, user_create):
        response = client.post("/api/user/", json=user_create.model_dump())
        assert response.status_code == 201
        assert response.json().get('username') == user_create.username
        assert response.json().get('is_admin') == user_create.is_admin

    def test_get_user_me(self, users):
        test_user = users['correct'][0]
        response = client.get("/api/user/me")
        assert response.status_code == 200
        assert response.json().get('username') == test_user['username']
        assert response.json().get('is_admin') == True

    def test_get_user(self, user):
        response = client.get(f"/api/user/{user.username}")
        assert response.status_code == 200
        assert UserBase.model_validate(user) == UserBase.model_validate(response.json())

    def test_delete_user(self, user):
        response = client.delete(f"/api/user/{user.username}")
        assert response.status_code == 204
        response = client.get("/api/user/")
        assert response.status_code == 200
        assert UserBase.model_validate(user) not in [UserBase.model_validate(u) for u in response.json()]

    def test_patch_user(self, user):
        user.is_admin = not user.is_admin
        response = client.patch(f"/api/user/{user.username}",
                                json={'is_admin': user.is_admin,
                                      'password': fake.password(length=fake.random_int(min=8, max=32))})
        assert response.status_code == 200
        assert UserBase.model_validate(user) == UserBase.model_validate(response.json())

    def test_post_logout(self):
        response = client.post("/api/logout")
        assert response.status_code == 204


class TestViewer:
    def test_post_login(self, users):
        test_user = users['correct'][1]
        response = client.post("/api/login", json=test_user)
        assert response.status_code == 200
        assert response.json().get('username') == test_user['username']

    def test_get_genres(self, genre):
        response = client.get("/api/genre/")
        assert response.status_code == 200
        assert genre in [Genre.model_validate(r) for r in response.json()]

    def test_get_genre(self, genre):
        response = client.get(f"/api/genre/{genre.id}")
        assert response.status_code == 200
        assert Genre.model_validate(response.json()) == genre

    def test_get_music(self, music_item):
        response = client.get("/api/music/", params={'size': fake.random_int(min=50, max=100)})
        assert response.status_code == 200
        assert MusicRead.model_validate(music_item) in [MusicRead.model_validate(r) for r in response.json().get('items')]

    def test_post_music_search(self, music_item):
        for search_query in generate_music_search_queries_matching(music_item):
            music_search_query = MusicSearchQuery(**search_query)
            music_search_query.random = choice([None, True, False])
            music_search_query.sort_by = choice([None] + list(MusicSearchQuerySortByEnum))
            music_search_query.sort_order = choice([None] + list(SortOrderEnum))
            response = client.post("/api/music/search", params={'size': fake.random_int(min=50, max=100)},
                                   json=music_search_query.model_dump())
            assert response.status_code == 200
            assert MusicRead.model_validate(music_item) in [MusicRead.model_validate(r) for r in response.json().get('items')]

    def test_get_music_item(self, music_item):
        response = client.get(f"/api/music/{music_item.id}")
        assert response.status_code == 200
        assert MusicRead.model_validate(response.json()) == MusicRead.model_validate(music_item)

    def test_get_music_cover(self, music_item):
        response = client.get(f"/api/music/{music_item.id}/cover")
        with NamedTemporaryFile(mode='wb') as f:
            f.write(response.content)
            assert response.status_code == 200
            assert cmp(f.name, join(settings.IMAGE_DIRECTORY, music_item.cover))

    def test_get_music_media(self, music_item):
        response = client.get(f"/api/music/{music_item.id}")
        assert response.status_code == 200
        music_item_path = response.json().get('path')
        response = client.get(f"/api/music/{music_item.id}/media")
        with NamedTemporaryFile(mode='wb') as f:
            f.write(response.content)
            assert response.status_code == 200
            assert cmp(f.name, music_item_path)

    def test_get_playlists(self, playlist, users):
        user_playlist = playlist(owner_username=users['correct'][1]['username'])
        response = client.get("/api/playlist/", params={'size': fake.random_int(min=50, max=100)})
        assert response.status_code == 200
        assert PlaylistRead.model_validate(user_playlist) in [PlaylistRead.model_validate(r) for r in response.json().get('items')]

    def test_post_playlist(self, playlist_create):
        response = client.post("/api/playlist/", json=playlist_create.model_dump())
        assert response.status_code == 201
        assert response.json().get('name') == playlist_create.name

    def test_post_playlist_search(self, playlist, users):
        user_playlist = playlist(owner_username=users['correct'][1]['username'])
        for search_query in generate_playlist_search_queries_matching(user_playlist):
            playlist_search_query = PlaylistSearchQuery(**search_query)
            playlist_search_query.sort_by = choice([None] + list(PlaylistSearchQuerySortByEnum))
            playlist_search_query.sort_order = choice([None] + list(SortOrderEnum))
            response = client.post("/api/playlist/search", params={'size': fake.random_int(min=50, max=100)},
                                   json=playlist_search_query.model_dump())
            assert response.status_code == 200
            assert PlaylistRead.model_validate(user_playlist) in [PlaylistRead.model_validate(r) for r in response.json().get('items')]

    def test_get_playlist(self, playlist, users):
        user_playlist = playlist(owner_username=users['correct'][1]['username'])
        response = client.get(f"/api/playlist/{user_playlist.id}")
        assert response.status_code == 200
        assert PlaylistRead.model_validate(response.json()) == PlaylistRead.model_validate(user_playlist)

    def test_patch_playlist(self, playlist, users):
        user_playlist = playlist(owner_username=users['correct'][1]['username'])
        user_playlist.name = fake.city()
        response = client.patch(f"/api/playlist/{user_playlist.id}", json={'name': user_playlist.name})
        assert response.status_code == 200
        assert response.json().get('name') == user_playlist.name

    def test_delete_playlist(self, playlist, users):
        user_playlist = playlist(owner_username=users['correct'][1]['username'])
        response = client.delete(f"/api/playlist/{user_playlist.id}")
        assert response.status_code == 204
        response = client.get("/api/playlist/", params={'size': fake.random_int(min=50, max=100)})
        assert response.status_code == 200
        assert PlaylistRead.model_validate(user_playlist) not in [PlaylistRead.model_validate(r) for r in response.json().get('items')]

    def test_get_playlist_export(self, playlist, users):
        user_playlist = playlist(owner_username=users['correct'][1]['username'])
        response = client.get(f"/api/playlist/{user_playlist.id}/export")
        assert response.status_code == 200

    def test_post_playlist_item(self, playlist_item_create, users):
        user_playlist_item_create = playlist_item_create(owner_username=users['correct'][1]['username'])
        response = client.post("/api/playlist_item/", json=user_playlist_item_create.model_dump())
        assert response.status_code == 201

    def test_delete_playlist_item(self, playlist_item, users):
        user_playlist_item = playlist_item(owner_username=users['correct'][1]['username'])
        response = client.delete(f"/api/playlist_item/{user_playlist_item.id}")
        assert response.status_code == 204
        response = client.get(f"/api/playlist/{user_playlist_item.playlist_id}")
        assert response.status_code == 200
        assert (PlaylistItemRead.model_validate(user_playlist_item) not in
                PlaylistRead.model_validate(response.json()).playlist_items)

    def test_patch_playlist_item(self, playlist_item, users):
        user_playlist_item = playlist_item(owner_username=users['correct'][1]['username'])
        user_playlist_item.order = fake.random_int(min=0, max=90)
        response = client.patch(f"/api/playlist_item/{user_playlist_item.id}",
                                json={'order': user_playlist_item.order})
        assert response.status_code == 200
        response = client.get(f"/api/playlist/{user_playlist_item.playlist_id}")
        assert response.status_code == 200
        assert (PlaylistItemRead.model_validate(user_playlist_item) in
                PlaylistRead.model_validate(response.json()).playlist_items)

    def test_get_user_me(self, users):
        test_user = users['correct'][1]
        response = client.get("/api/user/me")
        assert response.status_code == 200
        assert response.json().get('username') == test_user['username']
        assert response.json().get('is_admin') == False

    def test_patch_user_me(self, users):
        test_user = users['correct'][1]
        response = client.patch("/api/user/me", json={'password': fake.password(length=fake.random_int(min=8, max=32))})
        assert response.status_code == 200
        assert response.json().get('username') == test_user['username']
        assert response.json().get('is_admin') == False

    def test_post_logout(self):
        response = client.post("/api/logout")
        assert response.status_code == 204
