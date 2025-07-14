from fastapi import APIRouter
from mixmatch.api.endpoints import genres, health, login, playlists, playlist_items, tasks, tracks, users

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(login.router)
api_router.include_router(genres.router, prefix="/genres")
api_router.include_router(playlists.router, prefix="/playlists")
api_router.include_router(playlist_items.router, prefix="/playlist_items")
api_router.include_router(tasks.router, prefix="/tasks")
api_router.include_router(tracks.router, prefix="/tracks")
api_router.include_router(users.router, prefix="/users")
