from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from alembic.util import status
from fastapi import HTTPException, status
from fastapi.params import Depends
from jwt import InvalidTokenError

from core.config import pwd_context, SECRET_KEY, ALGORITHM, oauth2_scheme
from core.models import User, db_helper
from users.crud import get_user_by_username
from users.schemas import TokenData


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


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User | HTTPException:
    credentials_exeptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        details="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        pauload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = pauload.get("sub")
        if username is None:
            raise credentials_exeptions
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exeptions
    async with db_helper.session_factory() as session:
        user = await get_user_by_username(session=session, username=token_data.username)
        if user is None:
            raise credentials_exeptions
        return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, details="Inactive user")
    return current_user
