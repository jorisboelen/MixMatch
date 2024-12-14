from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from secrets import token_hex
from sqlmodel import Session
from typing import Annotated

from mixmatch.core.settings import settings
from mixmatch.db import crud
from mixmatch.db.database import get_db
from mixmatch.db.models import UserLogin, UserSession

router = APIRouter()


@router.post("/login", response_model=UserSession, status_code=200)
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    ph = PasswordHasher()
    db_user = crud.get_user(db=db, username=user.username)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username and/or password")
    try:
        if ph.verify(db_user.password, user.password):
            if ph.check_needs_rehash(db_user.password):
                crud.update_user_password(db=db, db_user=db_user, hashed_password=ph.hash(user.password))
            token = UserSession(token=token_hex(), username=user.username,
                                expires=datetime.now() + timedelta(seconds=settings.SESSION_EXPIRE_SECONDS))
            crud.create_user_session(db=db, user_session=token)
            response.set_cookie(key="session_token", value=token.token, expires=settings.SESSION_EXPIRE_SECONDS)
            return token
    except VerifyMismatchError:
        raise HTTPException(status_code=401, detail="Invalid username and/or password")


@router.post("/logout", status_code=204)
def logout(response: Response, session_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    if session_token:
        crud.remove_user_session(db=db, session_token=session_token)
        response.delete_cookie(key="session_token")
