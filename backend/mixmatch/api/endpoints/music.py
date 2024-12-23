from fastapi import APIRouter, Depends, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from fastapi_pagination import Page
from os import path, unlink
from sqlmodel import Session

from mixmatch.api.utils import require_admin_permissions as admin_permissions
from mixmatch.core.settings import APPLICATION_ASSETS_DIRECTORY, settings
from mixmatch.db import crud
from mixmatch.db.database import get_db
from mixmatch.db.models import Genre, MusicSearchQuery, MusicRead, MusicUpdate
from mixmatch.file import MusicFile

router = APIRouter()


@router.get("/", response_model=Page[MusicRead], status_code=200)
def read_music_items(db: Session = Depends(get_db)):
    music_items = crud.get_music_items_paginated(db)
    return music_items


@router.post("/search", response_model=Page[MusicRead], status_code=200)
def search_music_items(music_search_query: MusicSearchQuery, db: Session = Depends(get_db)):
    music_items = crud.search_music_items_paginated(db, music_search_query)
    return music_items


@router.get("/{music_id}", response_model=MusicRead, status_code=200)
def read_music_item(music_id: int, db: Session = Depends(get_db)):
    music_item = crud.get_music_item(db=db, music_id=music_id)
    if not music_item:
        raise HTTPException(status_code=404, detail="Music item not found")
    return music_item


@router.get("/{music_id}/cover", response_class=FileResponse, status_code=200)
def read_music_item_cover(music_id: int, db: Session = Depends(get_db)):
    music_item = crud.get_music_item(db=db, music_id=music_id)
    if not music_item:
        raise HTTPException(status_code=404, detail="Music item not found")
    elif music_item.cover:
        headers = {'Content-Disposition': f'attachment; filename={str(music_item.cover)}',
                   'X-Accel-Redirect': f'/image/{str(music_item.cover)}'}
        return FileResponse(path.join(settings.IMAGE_DIRECTORY, str(music_item.cover)), headers=headers)
    else:
        headers = {'Content-Disposition': 'attachment; filename=cover.png'}
        return FileResponse(path.join(APPLICATION_ASSETS_DIRECTORY, "cover.png"), headers=headers)


@router.put("/{music_id}/cover", dependencies=[Depends(admin_permissions)], status_code=204)
def update_music_item_cover(music_id: int, music_cover: UploadFile, db: Session = Depends(get_db)):
    db_music_item = crud.get_music_item(db=db, music_id=music_id)
    if not db_music_item:
        raise HTTPException(status_code=404, detail="Music item not found")
    if music_cover.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=415, detail="Unsupported image format")

    music_file = MusicFile(db_music_item.path)
    music_file.update_cover(cover_data=music_cover.file, cover_mime=music_cover.content_type)
    genre = crud.get_or_create_genre(db=db, genre=Genre(name=music_file.genre))
    crud.update_music_item(db=db, music_item=db_music_item,
                           music_item_data={**music_file.to_dict(), **{'genre': genre}})


@router.get("/{music_id}/media", response_class=FileResponse, status_code=200)
def read_music_item_media(music_id: int, db: Session = Depends(get_db)):
    music_item = crud.get_music_item(db=db, music_id=music_id)
    if not music_item:
        raise HTTPException(status_code=404, detail="Music item not found")
    else:
        headers = {'Content-Disposition': f'attachment; filename={path.basename(music_item.path)}',
                   'X-Accel-Redirect': f'/music/{path.relpath(music_item.path, settings.MUSIC_DIRECTORY)}'}
        return FileResponse(path=music_item.path, headers=headers)


@router.patch("/{music_id}", response_model=MusicRead, dependencies=[Depends(admin_permissions)], status_code=200)
def patch_music_item(music_id: int, music_item: MusicUpdate, db: Session = Depends(get_db)):
    db_music_item = crud.get_music_item(db=db, music_id=music_id)
    if not db_music_item:
        raise HTTPException(status_code=404, detail="Music item not found")
    if not music_item.genre_id:
        genre = crud.get_genre(db=db, genre_id=db_music_item.genre_id)
    else:
        genre = crud.get_genre(db=db, genre_id=music_item.genre_id)
    music_file = MusicFile(db_music_item.path)
    music_file.update_music_data(music_data={**music_item.model_dump(exclude_unset=True), **{'genre': genre.name}})
    return crud.update_music_item(db=db, music_item=db_music_item,
                                  music_item_data={**music_file.to_dict(), **{'genre': genre},
                                                   **{'rating': music_item.rating if music_item.rating >=0
                                                   else db_music_item.rating}})


@router.delete("/{music_id}", dependencies=[Depends(admin_permissions)], status_code=204)
def delete_music_item(music_id: int, db: Session = Depends(get_db)):
    music_item = crud.get_music_item(db=db, music_id=music_id)
    if not music_item:
        raise HTTPException(status_code=404, detail="Music item not found")
    unlink(music_item.path)
    crud.remove_music_item(db=db, music_item=music_item)
