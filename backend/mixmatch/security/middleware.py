from datetime import datetime
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from mixmatch.db.models import UserSession


SESSION_TOKEN_LIST = {}
AUTH_INCLUDED_PREFIX = '/api/'
AUTH_EXCLUDED_URLS = ['/api/login', '/api/logout', '/api/docs', '/api/openapi.json']


class SessionCookieMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith(AUTH_INCLUDED_PREFIX) and request.url.path not in AUTH_EXCLUDED_URLS:
            session_token = request.cookies.get('session_token')
            session: UserSession | None = SESSION_TOKEN_LIST.get(session_token, None)

            if not session_token:
                return JSONResponse(status_code=403, content={"detail": "Not logged in"})
            elif not session:
                return JSONResponse(status_code=403, content={"detail": "Session token invalid or expired"})
            elif session and session.expires < datetime.now():
                return JSONResponse(status_code=403, content={"detail": "Session expired"})
        response = await call_next(request)
        return response
