import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from core.models import db_helper
from users.crud import get_user_by_username, hash_password

security = HTTPBasic()


async def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):

    current_username_bytes = credentials.username.encode("utf8")
    current_password_bytes = hash_password(credentials.password)
    async with db_helper.session_factory() as session:
        correct_user = await get_user_by_username(
            username=credentials.username, session=session
        )
        correct_username_bytes = str(correct_user.username)
        correct_password_bytes = await get_user_by_username(
            username=credentials.username, session=session
        )
    is_correct_username = secrets.compare_digest(
        current_username_bytes , correct_username_bytes.encode("utf-8")
    )
    print("------------------------------------------------")
    print(current_username_bytes, correct_username_bytes)
    print("------------------------------------------------")

    is_correct_password = secrets.compare_digest(
        current_password_bytes.encode("utf-8"), correct_password_bytes.password.encode("utf8")
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
