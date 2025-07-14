from argon2 import PasswordHasher
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlmodel import Session
from typing import Annotated

from mixmatch.api.utils import get_current_user, require_admin_permissions as admin_permissions
from mixmatch.db import crud
from mixmatch.db.database import get_db
from mixmatch.db.models import UserBase, UserCreate, UserUpdate, UserCurrentUpdate, User

router = APIRouter()


@router.get("/", response_model=list[UserBase], dependencies=[Depends(admin_permissions)], status_code=200)
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users


@router.get("/me", response_model=UserBase, status_code=200)
def read_current_user(current_user: Annotated[User | None, Depends(get_current_user)]):
    if current_user:
        return current_user


@router.patch("/me", response_model=UserBase, status_code=200)
def patch_current_user(current_user: Annotated[User | None, Depends(get_current_user)],
                       user: UserCurrentUpdate, db: Session = Depends(get_db)):
    if user.password:
        user.password = PasswordHasher().hash(user.password)
    return crud.update_user(db=db, user=current_user, user_data=user.model_dump(exclude_unset=True))


@router.get("/{username}", response_model=UserBase, dependencies=[Depends(admin_permissions)], status_code=200)
def read_user(username: str, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserBase, dependencies=[Depends(admin_permissions)], status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user.password = PasswordHasher().hash(user.password)
    return crud.create_user(db=db, user=User.model_validate(user))


@router.delete("/{username}", dependencies=[Depends(admin_permissions)], status_code=204)
def delete_user(username: str, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.remove_user(db=db, user=user)


@router.patch("/{username}", response_model=UserBase, dependencies=[Depends(admin_permissions)], status_code=200)
def patch_user(username: str, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, username=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password:
        user.password = PasswordHasher().hash(user.password)
    return crud.update_user(db=db, user=db_user, user_data=user.model_dump(exclude_unset=True))
