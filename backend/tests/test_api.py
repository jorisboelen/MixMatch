from fastapi.testclient import TestClient
from filecmp import cmp
from mixmatch.app import app
from mixmatch.core.settings import settings
from mixmatch.db.models import Genre, SortOrderEnum, TrackRead, TrackSearchQuery, TrackSearchQuerySortByEnum
from mixmatch.db.models import PlaylistRead, PlaylistItemRead, PlaylistSearchQuery, PlaylistSearchQuerySortByEnum
from mixmatch.db.models import UserBase
from os.path import join
from random import choice
from tempfile import NamedTemporaryFile
from .fixtures import alembic_upgrade, genre, genre_create, playlist, playlist_create, track, track_cover
from .fixtures import playlist_item, playlist_item_create, tasks, user_create, user, users, user_tokens
from .utils import fake, generate_playlist_search_queries_matching, generate_track_search_queries_matching

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
        response = client.post("/api/genres/", json=genre_create.model_dump())
        assert response.status_code == 201
        assert response.json().get('name') == genre_create.name

    def test_delete_genre(self, genre):
        response = client.delete(f"/api/genres/{genre.id}")
        assert response.status_code == 204
        response = client.get("/api/genres/")
        assert response.status_code == 200
        assert genre not in [Genre.model_validate(r) for r in response.json()]

    def test_patch_track(self, track, genre):
        track.artist = fake.country()
        track.title = fake.name()
        track.album = fake.city()
        track.genre_id = genre.id
        track.date = fake.year()
        track.rating = fake.random_int(min=0, max=5)
        response = client.patch(f"/api/tracks/{track.id}",
                                json={'artist': track.artist, 'title': track.title,
                                      'album': track.album, 'genre_id': track.genre_id,
                                      'date': track.date, 'rating': track.rating})
        assert response.status_code == 200
        assert response.json().get('artist') == track.artist
        assert response.json().get('title') == track.title
        assert response.json().get('album') == track.album
        assert response.json().get('genre').get('id') == track.genre_id
        assert response.json().get('date') == track.date
        assert response.json().get('rating') == track.rating

    def test_delete_track(self, track):
        response = client.delete(f"/api/tracks/{track.id}")
        assert response.status_code == 204
        response = client.get("/api/tracks/", params={'size': 100})
        assert response.status_code == 200
        assert TrackRead.model_validate(track) not in [TrackRead.model_validate(r) for r in response.json().get('items')]

    def test_put_track_cover(self, track, track_cover):
        response = client.put(f"/api/tracks/{track.id}/cover", files={'track_cover': open(track_cover, 'rb')})
        assert response.status_code == 204
        response = client.get(f"/api/tracks/{track.id}/cover")
        with NamedTemporaryFile(mode='wb') as f:
            f.write(response.content)
            assert response.status_code == 200
            assert cmp(f.name, track_cover)

    def test_get_tasks(self, tasks):
        response = client.get("/api/tasks/")
        assert response.status_code == 200
        assert response.json() == tasks

    def test_get_tasks_running(self):
        response = client.get("/api/tasks/running")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_task(self, tasks):
        response = client.get(f"/api/tasks/{tasks[0].get('id')}")
        assert response.status_code == 200
        assert response.json() == tasks[0]
        response = client.get(f"/api/tasks/{tasks[1].get('id')}")
        assert response.status_code == 200
        assert response.json() == tasks[1]

    def test_get_users(self, users):
        response = client.get("/api/users/")
        assert response.status_code == 200
        assert UserBase.model_validate(users['correct'][0]) in [UserBase.model_validate(u) for u in response.json()]
        assert UserBase.model_validate(users['correct'][1]) in [UserBase.model_validate(u) for u in response.json()]

    def test_post_user(self, user_create):
        response = client.post("/api/users/", json=user_create.model_dump())
        assert response.status_code == 201
        assert response.json().get('username') == user_create.username
        assert response.json().get('is_admin') == user_create.is_admin

    def test_get_user_me(self, users):
        test_user = users['correct'][0]
        response = client.get("/api/users/me")
        assert response.status_code == 200
        assert response.json().get('username') == test_user['username']
        assert response.json().get('is_admin') == True

    def test_get_user(self, user):
        response = client.get(f"/api/users/{user.username}")
        assert response.status_code == 200
        assert UserBase.model_validate(user) == UserBase.model_validate(response.json())

    def test_delete_user(self, user):
        response = client.delete(f"/api/users/{user.username}")
        assert response.status_code == 204
        response = client.get("/api/users/")
        assert response.status_code == 200
        assert UserBase.model_validate(user) not in [UserBase.model_validate(u) for u in response.json()]

    def test_patch_user(self, user):
        user.is_admin = not user.is_admin
        response = client.patch(f"/api/users/{user.username}",
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
        response = client.get("/api/genres/")
        assert response.status_code == 200
        assert genre in [Genre.model_validate(r) for r in response.json()]

    def test_get_genre(self, genre):
        response = client.get(f"/api/genres/{genre.id}")
        assert response.status_code == 200
        assert Genre.model_validate(response.json()) == genre

    def test_get_tracks(self, track):
        response = client.get("/api/tracks/", params={'size': fake.random_int(min=50, max=100)})
        assert response.status_code == 200
        assert TrackRead.model_validate(track) in [TrackRead.model_validate(r) for r in response.json().get('items')]

    def test_post_track_search(self, track):
        for search_query in generate_track_search_queries_matching(track):
            track_search_query = TrackSearchQuery(**search_query)
            track_search_query.random = choice([None, True, False])
            track_search_query.sort_by = choice([None] + list(TrackSearchQuerySortByEnum))
            track_search_query.sort_order = choice([None] + list(SortOrderEnum))
            response = client.post("/api/tracks/search", params={'size': fake.random_int(min=50, max=100)},
                                   json=track_search_query.model_dump())
            assert response.status_code == 200
            assert TrackRead.model_validate(track) in [TrackRead.model_validate(r) for r in response.json().get('items')]

    def test_get_track(self, track):
        response = client.get(f"/api/tracks/{track.id}")
        assert response.status_code == 200
        assert TrackRead.model_validate(response.json()) == TrackRead.model_validate(track)

    def test_get_track_cover(self, track):
        response = client.get(f"/api/tracks/{track.id}/cover")
        with NamedTemporaryFile(mode='wb') as f:
            f.write(response.content)
            assert response.status_code == 200
            assert cmp(f.name, join(settings.IMAGE_DIRECTORY, track.cover))

    def test_get_track_media(self, track):
        response = client.get(f"/api/tracks/{track.id}")
        assert response.status_code == 200
        track_path = response.json().get('path')
        response = client.get(f"/api/tracks/{track.id}/media")
        with NamedTemporaryFile(mode='wb') as f:
            f.write(response.content)
            assert response.status_code == 200
            assert cmp(f.name, track_path)

    def test_get_playlists(self, playlist, users):
        user_playlist = playlist(owner_username=users['correct'][1]['username'])
        response = client.get("/api/playlists/", params={'size': fake.random_int(min=50, max=100)})
        assert response.status_code == 200
        assert PlaylistRead.model_validate(user_playlist) in [PlaylistRead.model_validate(r) for r in response.json().get('items')]

    def test_post_playlist(self, playlist_create):
        response = client.post("/api/playlists/", json=playlist_create.model_dump())
        assert response.status_code == 201
        assert response.json().get('name') == playlist_create.name

    def test_post_playlist_search(self, playlist, users):
        user_playlist = playlist(owner_username=users['correct'][1]['username'])
        for search_query in generate_playlist_search_queries_matching(user_playlist):
            playlist_search_query = PlaylistSearchQuery(**search_query)
            playlist_search_query.sort_by = choice([None] + list(PlaylistSearchQuerySortByEnum))
            playlist_search_query.sort_order = choice([None] + list(SortOrderEnum))
            response = client.post("/api/playlists/search", params={'size': fake.random_int(min=50, max=100)},
                                   json=playlist_search_query.model_dump())
            assert response.status_code == 200
            assert PlaylistRead.model_validate(user_playlist) in [PlaylistRead.model_validate(r) for r in response.json().get('items')]

    def test_get_playlist(self, playlist, users):
        user_playlist = playlist(owner_username=users['correct'][1]['username'])
        response = client.get(f"/api/playlists/{user_playlist.id}")
        assert response.status_code == 200
        assert PlaylistRead.model_validate(response.json()) == PlaylistRead.model_validate(user_playlist)

    def test_patch_playlist(self, playlist, users):
        user_playlist = playlist(owner_username=users['correct'][1]['username'])
        user_playlist.name = fake.city()
        response = client.patch(f"/api/playlists/{user_playlist.id}", json={'name': user_playlist.name})
        assert response.status_code == 200
        assert response.json().get('name') == user_playlist.name

    def test_delete_playlist(self, playlist, users):
        user_playlist = playlist(owner_username=users['correct'][1]['username'])
        response = client.delete(f"/api/playlists/{user_playlist.id}")
        assert response.status_code == 204
        response = client.get("/api/playlists/", params={'size': fake.random_int(min=50, max=100)})
        assert response.status_code == 200
        assert PlaylistRead.model_validate(user_playlist) not in [PlaylistRead.model_validate(r) for r in response.json().get('items')]

    def test_get_playlist_export(self, playlist, users):
        user_playlist = playlist(owner_username=users['correct'][1]['username'])
        response = client.get(f"/api/playlists/{user_playlist.id}/export")
        assert response.status_code == 200

    def test_post_playlist_item(self, playlist_item_create, users):
        user_playlist_item_create = playlist_item_create(owner_username=users['correct'][1]['username'])
        response = client.post("/api/playlist_items/", json=user_playlist_item_create.model_dump())
        assert response.status_code == 201

    def test_delete_playlist_item(self, playlist_item, users):
        user_playlist_item = playlist_item(owner_username=users['correct'][1]['username'])
        response = client.delete(f"/api/playlist_items/{user_playlist_item.id}")
        assert response.status_code == 204
        response = client.get(f"/api/playlists/{user_playlist_item.playlist_id}")
        assert response.status_code == 200
        assert (PlaylistItemRead.model_validate(user_playlist_item) not in
                PlaylistRead.model_validate(response.json()).playlist_items)

    def test_patch_playlist_item(self, playlist_item, users):
        user_playlist_item = playlist_item(owner_username=users['correct'][1]['username'])
        user_playlist_item.order = fake.random_int(min=0, max=90)
        response = client.patch(f"/api/playlist_items/{user_playlist_item.id}",
                                json={'order': user_playlist_item.order})
        assert response.status_code == 200
        response = client.get(f"/api/playlists/{user_playlist_item.playlist_id}")
        assert response.status_code == 200
        assert (PlaylistItemRead.model_validate(user_playlist_item) in
                PlaylistRead.model_validate(response.json()).playlist_items)

    def test_get_user_me(self, users):
        test_user = users['correct'][1]
        response = client.get("/api/users/me")
        assert response.status_code == 200
        assert response.json().get('username') == test_user['username']
        assert response.json().get('is_admin') == False

    def test_patch_user_me(self, users):
        test_user = users['correct'][1]
        response = client.patch("/api/users/me", json={'password': fake.password(length=fake.random_int(min=8, max=32))})
        assert response.status_code == 200
        assert response.json().get('username') == test_user['username']
        assert response.json().get('is_admin') == False

    def test_post_logout(self):
        response = client.post("/api/logout")
        assert response.status_code == 204
