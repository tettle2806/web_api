from fastapi import Request

from core.config import pwd_context
from exeptions import TokenNoFoundException


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise TokenNoFoundException
    return token
