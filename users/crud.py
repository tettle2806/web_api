"""
Create
Read
Update
Delete
"""

from typing import Annotated, Union

import hashlib

from pydantic import EmailStr
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


async def create_user_crud(
    session: AsyncSession, username: str, email: str, password: str
) -> User:
    user = User(username=username, email=email, password=password)
    await session.add(user)
    await session.commit()
    return user


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


async def get_user_by_username(
    session: AsyncSession, email: EmailStr
) -> Union[User, None]:
    try:
        stmt = select(User).where(User.email == email)
        user: User | None = await session.scalar(stmt)
        return user
    except Exception as e:
        print(e)
        return None
