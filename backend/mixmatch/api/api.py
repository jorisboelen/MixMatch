from fastapi import APIRouter
from mixmatch.api.endpoints import login, genre, music, playlist, playlist_item, task, user

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(genre.router, prefix="/genre")
api_router.include_router(music.router, prefix="/music")
api_router.include_router(playlist.router, prefix="/playlist")
api_router.include_router(playlist_item.router, prefix="/playlist_item")
api_router.include_router(task.router, prefix="/task")
api_router.include_router(user.router, prefix="/user")
