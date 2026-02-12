
import datetime
from http import HTTPStatus
from itertools import dropwhile
from exceptiongroup import catch
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from services.auth import decode_token

async def auth_middleware( request: Request):
    authorization_header = request.headers.get('Authorization')
    token= authorization_header.split()[1]
    try:
        auth_data=decode_token(token)        
        request.state.auth_data = auth_data
    except:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="token expired")




