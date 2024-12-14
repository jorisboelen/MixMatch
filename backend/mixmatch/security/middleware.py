from datetime import datetime
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from mixmatch.db import crud
from mixmatch.db.database import get_db


AUTH_INCLUDED_PREFIX = '/api/'
AUTH_EXCLUDED_URLS = ['/api/health', '/api/login', '/api/logout', '/api/docs', '/api/openapi.json']


class SessionCookieMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith(AUTH_INCLUDED_PREFIX) and request.url.path not in AUTH_EXCLUDED_URLS:
            session_token = request.cookies.get('session_token')
            if not session_token:
                return JSONResponse(status_code=403, content={"detail": "Not logged in"})
            else:
                user_session = crud.get_user_session_cached(session_token=session_token)
                if not user_session:
                    return JSONResponse(status_code=403, content={"detail": "Session token invalid or expired"})
                elif user_session.expires < datetime.now():
                    crud.remove_user_session(db=next(get_db()), session_token=user_session.token)
                    return JSONResponse(status_code=403, content={"detail": "Session expired"})
        response = await call_next(request)
        return response
