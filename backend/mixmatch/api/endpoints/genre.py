from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlmodel import Session

from mixmatch.api.utils import require_admin_permissions as admin_permissions
from mixmatch.db import crud
from mixmatch.db.database import get_db
from mixmatch.db.models import Genre, GenreCreate, GenreRead

router = APIRouter()


@router.get("/", response_model=list[GenreRead], status_code=200)
def read_genres(db: Session = Depends(get_db)):
    genres = crud.get_genres(db)
    return genres


@router.post("/", response_model=GenreRead, dependencies=[Depends(admin_permissions)], status_code=201)
def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    return crud.get_or_create_genre(db=db, genre=Genre.model_validate(genre))


@router.get("/{genre_id}", response_model=GenreRead, status_code=200)
def read_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = crud.get_genre(db=db, genre_id=genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre


@router.delete("/{genre_id}", dependencies=[Depends(admin_permissions)], status_code=204)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = crud.get_genre(db=db, genre_id=genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    crud.remove_genre(db=db, genre=genre)
