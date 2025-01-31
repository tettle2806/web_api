from datetime import datetime, timedelta, timezone

import jwt

from core.config import pwd_context, SECRET_KEY, ALGORITHM
from core.models import User, db_helper
from users.crud import get_user_by_username


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str) -> User | bool:
    async with db_helper.session_factory() as session:
        user = await get_user_by_username(session=session, username=username)
        if not user:
            return False
        if not await verify_password(password, user.password):
            return False
        return user


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
