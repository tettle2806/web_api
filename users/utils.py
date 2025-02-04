import hashlib
from datetime import datetime, timedelta
from typing import Union, Any
from uuid import UUID

import jwt
from passlib.context import CryptContext

from core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    JWT_SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    JWT_REFRESH_SECRET_KEY,
)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed_pass: str) -> bool:
    if password == hashed_pass:
        return True
    return False


def create_access_token(
    uuid: UUID, subject: Union[str, Any], expires_delta: int = None
) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject), "uuid": str(uuid)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    uuid: UUID, subject: Union[str, Any], expires_delta: int = None
) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject), "uuid": str(uuid)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt
