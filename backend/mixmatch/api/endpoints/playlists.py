from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import PlainTextResponse
from fastapi_pagination import Page
from os import linesep
from sqlalchemy.sql.expression import func
from sqlmodel import Session
from typing import Annotated

from mixmatch.api.utils import get_current_user
from mixmatch.db import crud
from mixmatch.db.database import get_db
from mixmatch.db.models import Playlist, PlaylistCreate, PlaylistRead, PlaylistUpdate, PlaylistSearchQuery, User

router = APIRouter()


@router.get("/", response_model=Page[PlaylistRead], status_code=200)
def read_playlists(current_user: Annotated[User | None, Depends(get_current_user)], db: Session = Depends(get_db)):
    playlists = crud.get_playlists_paginated(db=db, owner=current_user)
    return playlists


@router.post("/search", response_model=Page[PlaylistRead], status_code=200)
def search_playlists(current_user: Annotated[User | None, Depends(get_current_user)],
                     playlist_search_query: PlaylistSearchQuery, db: Session = Depends(get_db)):
    playlists = crud.search_playlists_paginated(db=db, owner=current_user, playlist_search_query=playlist_search_query)
    return playlists


@router.post("/", response_model=PlaylistRead, status_code=201)
def create_playlist(current_user: Annotated[User | None, Depends(get_current_user)],
                    playlist: PlaylistCreate, db: Session = Depends(get_db)):
    return crud.create_playlist(db=db, playlist=Playlist.model_validate(playlist), owner=current_user)


@router.get("/{playlist_id}", response_model=PlaylistRead, status_code=200)
def read_playlist(current_user: Annotated[User | None, Depends(get_current_user)], playlist_id: int,
                  db: Session = Depends(get_db)):
    playlist = crud.get_playlist(db=db, playlist_id=playlist_id, owner=current_user)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist


@router.get("/{playlist_id}/export", response_class=PlainTextResponse, status_code=200)
def export_playlist(current_user: Annotated[User | None, Depends(get_current_user)], playlist_id: int,
                    db: Session = Depends(get_db)):
    playlist = crud.get_playlist(db=db, playlist_id=playlist_id, owner=current_user)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return linesep.join([f'{i.order:02d}) {i.track.artist} - {i.track.title}' for i in playlist.playlist_items])


@router.patch("/{playlist_id}", response_model=PlaylistRead, status_code=200)
def patch_playlist(current_user: Annotated[User | None, Depends(get_current_user)],
                   playlist_id: int, playlist: PlaylistUpdate, db: Session = Depends(get_db)):
    db_playlist = crud.get_playlist(db=db, playlist_id=playlist_id, owner=current_user)
    if not db_playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return crud.update_playlist(db=db, playlist=db_playlist,
                                playlist_data={**playlist.model_dump(exclude_unset=True), **{'modified': func.now()}})


@router.delete("/{playlist_id}", status_code=204)
def delete_playlist(current_user: Annotated[User | None, Depends(get_current_user)],
                    playlist_id: int, db: Session = Depends(get_db)):
    playlist = crud.get_playlist(db=db, playlist_id=playlist_id, owner=current_user)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    crud.remove_playlist(db=db, playlist=playlist)
