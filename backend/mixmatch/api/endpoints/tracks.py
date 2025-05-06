from fastapi import APIRouter, Depends, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from fastapi_pagination import Page
from os import path, unlink
from pathlib import Path
from sqlmodel import Session

from mixmatch.api.utils import require_admin_permissions as admin_permissions
from mixmatch.core.settings import APPLICATION_ASSETS_DIRECTORY, settings
from mixmatch.db import crud
from mixmatch.db.database import get_db
from mixmatch.db.models import TrackSearchQuery, TrackRead, TrackUpdate
from mixmatch.file import mixmatch_file, MixMatchFileCover
from mixmatch.tasks.utils import save_cover

router = APIRouter()


@router.get("/", response_model=Page[TrackRead], status_code=200)
def read_track(db: Session = Depends(get_db)):
    tracks = crud.get_tracks_paginated(db)
    return tracks


@router.post("/search", response_model=Page[TrackRead], status_code=200)
def search_tracks(track_search_query: TrackSearchQuery, db: Session = Depends(get_db)):
    tracks = crud.search_tracks_paginated(db, track_search_query)
    return tracks


@router.get("/{track_id}", response_model=TrackRead, status_code=200)
def read_track(track_id: int, db: Session = Depends(get_db)):
    track = crud.get_track(db=db, track_id=track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track


@router.get("/{track_id}/cover", response_class=FileResponse, status_code=200)
def read_track_cover(track_id: int, db: Session = Depends(get_db)):
    track = crud.get_track(db=db, track_id=track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    elif track.cover:
        headers = {'Content-Disposition': f'attachment; filename={str(track.cover)}',
                   'X-Accel-Redirect': f'/image/{str(track.cover)}'}
        return FileResponse(path.join(settings.IMAGE_DIRECTORY, str(track.cover)), headers=headers)
    else:
        headers = {'Content-Disposition': 'attachment; filename=cover.png'}
        return FileResponse(path.join(APPLICATION_ASSETS_DIRECTORY, "cover.png"), headers=headers)


@router.put("/{track_id}/cover", dependencies=[Depends(admin_permissions)], status_code=204)
def update_track_cover(track_id: int, track_cover: UploadFile, db: Session = Depends(get_db)):
    db_track = crud.get_track(db=db, track_id=track_id)
    if not db_track:
        raise HTTPException(status_code=404, detail="Track not found")
    if track_cover.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=415, detail="Unsupported image format")

    music_file = mixmatch_file(file_path=Path(db_track.path))
    music_file.cover = MixMatchFileCover(data=track_cover.file.read(), mime=track_cover.content_type)
    music_file.save()
    cover = save_cover(music_file.cover)
    crud.update_track(db=db, track=db_track, track_data={'cover': cover, 'mtime': music_file.mtime})


@router.get("/{track_id}/media", response_class=FileResponse, status_code=200)
def read_track_media(track_id: int, db: Session = Depends(get_db)):
    track = crud.get_track(db=db, track_id=track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    else:
        headers = {'Content-Disposition': f'attachment; filename={path.basename(track.path)}',
                   'X-Accel-Redirect': f'/track/{path.relpath(track.path, settings.MUSIC_DIRECTORY)}'}
        return FileResponse(path=track.path, headers=headers)


@router.patch("/{track_id}", response_model=TrackRead, dependencies=[Depends(admin_permissions)], status_code=200)
def patch_track(track_id: int, track: TrackUpdate, db: Session = Depends(get_db)):
    db_track = crud.get_track(db=db, track_id=track_id)
    if not db_track:
        raise HTTPException(status_code=404, detail="Track not found")
    if not track.genre_id:
        genre = crud.get_genre(db=db, genre_id=db_track.genre_id)
    else:
        genre = crud.get_genre(db=db, genre_id=track.genre_id)
    music_file = mixmatch_file(file_path=Path(db_track.path))
    music_file.artist = track.artist
    music_file.title = track.title
    music_file.album = track.album
    music_file.genre = genre.name
    music_file.date = track.date
    music_file.save()
    return crud.update_track(db=db, track=db_track,
                             track_data={**music_file.model_dump(exclude={'cover', 'genre'}),
                                         **{'genre': genre,
                                            'rating': track.rating if track.rating >=0 else db_track.rating}})


@router.delete("/{track_id}", dependencies=[Depends(admin_permissions)], status_code=204)
def delete_track(track_id: int, db: Session = Depends(get_db)):
    track = crud.get_track(db=db, track_id=track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    unlink(track.path)
    crud.remove_track(db=db, track=track)
