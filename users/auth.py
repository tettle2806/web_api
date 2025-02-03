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


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str):
    return pwd_context.hash(password)

