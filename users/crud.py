"""
Create
Read
Update
Delete
"""
import hashlib

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from users.schemas import CreateUser


def create_user(user_in: CreateUser) -> dict:
    user = user_in.model_dump()
    return {
        "success": True,
        "user": user,
    }

async def create_user_crud(session: AsyncSession, username: str, email: str, password:str) -> User:
    user = User(username=username, email=email, password=password)
    session.add(user)
    await session.commit()
    print("user", user)
    return user

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()




