from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

from pydantic import EmailStr

from core.config import pwd_context
from core.models import db_helper
from .crud import get_user_by_username, hash_password
from users.schemas import UserDTO, Token


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str):
    return pwd_context.hash(password)


class UserAuth:

    async def create_access_token(self, data: dict, expires_delta: timedelta) -> str:
        pass

    async def decode_token(self, token: str):
        pass

    async def login_for_access_token(self, email: str, password: str) -> Token:
        pass

    async def validate_user(
        self, email: EmailStr, password: str
    ) -> Union[UserDTO, bool]:
        hashed = await hash_password(password)
        async with db_helper.session_factory() as session:
            user: UserDTO = await get_user_by_username(session=session, email=email)
        if user and user.password.__eq__(hashed):
            return user
        return False
