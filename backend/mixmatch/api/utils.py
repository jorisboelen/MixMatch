from fastapi import Cookie, Depends, HTTPException
from sqlmodel import Session
from typing import Annotated

from mixmatch.db import crud
from mixmatch.db.database import get_db


def get_current_user(session_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    if session_token:
        user_session = crud.get_user_session(db=db, session_token=session_token)
        if user_session:
            user = crud.get_user(db=db, username=user_session.username)
            return user


async def require_admin_permissions(session_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    if session_token:
        user_session = crud.get_user_session_cached(session_token=session_token)
        if user_session:
            if crud.get_user(db=db, username=user_session.username).is_admin:
                return
    raise HTTPException(status_code=403, detail={"detail": "Permission denied"})
