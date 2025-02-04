"""
Create
Read
Update
Delete
"""

import hashlib

from pydantic import EmailStr
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from core.models import User


async def create_user_crud(
    session: AsyncSession, username: str, email: EmailStr, password: str, uuid: UUID
) -> User:
    user = User(username=username, email=email, password=password, uuid=uuid)
    session.add(user)
    await session.commit()
    return user


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    # result: Result = await session.execute(stmt)
    # # user: User | None = result.scalar_one_or_none()
    # user: User | None = result.scalar_one()
    user: User | None = await session.scalar(stmt)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    user: User | None = await session.scalar(stmt)
    return user
