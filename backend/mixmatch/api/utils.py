from fastapi import Cookie, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session
from typing import Annotated

from mixmatch.db import crud
from mixmatch.db.database import get_db
from mixmatch.security.middleware import SESSION_TOKEN_LIST


def get_current_user(session_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    if session_token:
        session = SESSION_TOKEN_LIST.get(session_token)
        user = crud.get_user(db=db, username=session.username)
        return user


async def require_admin_permissions(session_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    if session_token:
        session = SESSION_TOKEN_LIST.get(session_token)
        if crud.get_user(db=db, username=session.username).is_admin:
            return
    raise HTTPException(status_code=403, detail={"detail": "Permission denied"})
