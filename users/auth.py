from fastapi import Request

from core.config import pwd_context
from exeptions import TokenNoFoundException


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise TokenNoFoundException
    return token
