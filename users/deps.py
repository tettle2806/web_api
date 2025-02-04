import asyncio
from datetime import datetime

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from core.models import db_helper
from users.crud import get_user_by_email
from .utils import ALGORITHM, JWT_SECRET_KEY

from users.schemas import TokenPayload, SystemUser

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


async def get_current_user(token: str = Depends(reuseable_oauth)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise credentials_exception

    except InvalidTokenError:
        raise
    async with db_helper.session_factory() as session:
        user = await get_user_by_email(session=session, email=email)
    if user is None:
        return credentials_exception
    return user
    # return SystemUser(uuid=user.uuid, email=user.email, password=user.password)
