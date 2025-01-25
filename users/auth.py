import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from users.crud import get_user_by_username, hash_password

security = HTTPBasic()

async def get_current_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)], session: AsyncSession
):

    current_username_bytes = credentials.username.encode("utf8")
    async with db_helper.session_factory() as session:
        correct_username_bytes = await get_user_by_username(username=credentials.username, session=session)
        correct_password_bytes = await get_user_by_username(username=credentials.username, session=session)
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes.username.encode("utf8")
    )
    current_password_bytes = hash_password(credentials.password.encode("utf8")).encode("utf8")

    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes.password.encode("utf8")
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
