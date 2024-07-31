from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.sql.expression import func
from sqlmodel import Session
from typing import Annotated

from mixmatch.api.utils import get_current_user
from mixmatch.db import crud
from mixmatch.db.database import get_db
from mixmatch.db.models import PlaylistItem, PlaylistItemCreate, PlaylistItemRead, PlaylistItemUpdate, User

router = APIRouter()


@router.post("/", response_model=PlaylistItemRead, status_code=201)
def create_playlist_item(current_user: Annotated[User | None, Depends(get_current_user)],
                         playlist_item: PlaylistItemCreate, db: Session = Depends(get_db)):
    music_item = crud.get_music_item(db=db, music_id=playlist_item.music_id)
    playlist = crud.get_playlist(db=db, playlist_id=playlist_item.playlist_id, owner=current_user)

    if not music_item:
        raise HTTPException(status_code=404, detail="Music item not found")
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    playlist = crud.update_playlist(db=db, playlist=playlist, playlist_data={'modified': func.now()})
    return crud.create_playlist_item(db=db, playlist_item=PlaylistItem(playlist=playlist, music=music_item,
                                                                       order=playlist_item.order))


@router.delete("/{playlist_item_id}", status_code=204)
def delete_playlist_item(current_user: Annotated[User | None, Depends(get_current_user)],
                         playlist_item_id: int, db: Session = Depends(get_db)):
    playlist_item = crud.get_playlist_item(db=db, playlist_item_id=playlist_item_id)
    if not playlist_item:
        raise HTTPException(status_code=404, detail="Playlist item not found")

    playlist = crud.get_playlist(db=db, playlist_id=playlist_item.playlist_id, owner=current_user)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    crud.update_playlist(db=db, playlist=playlist, playlist_data={'modified': func.now()})
    crud.remove_playlist_item(db=db, playlist_item=playlist_item)


@router.patch("/{playlist_item_id}", response_model=PlaylistItemRead, status_code=200)
def patch_playlist_item(current_user: Annotated[User | None, Depends(get_current_user)],
                        playlist_item_id: int, playlist_item: PlaylistItemUpdate, db: Session = Depends(get_db)):
    db_playlist_item = crud.get_playlist_item(db=db, playlist_item_id=playlist_item_id)
    if not db_playlist_item:
        raise HTTPException(status_code=404, detail="Playlist item not found")

    playlist = crud.get_playlist(db=db, playlist_id=db_playlist_item.playlist_id, owner=current_user)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    crud.update_playlist(db=db, playlist=playlist, playlist_data={'modified': func.now()})
    return crud.update_playlist_item(db=db, playlist_item=db_playlist_item,
                                     playlist_item_data=playlist_item.model_dump(exclude_unset=True))
