from core.config import pwd_context
from core.models import User
from users.crud import get_user_by_username


async def verify_password(plain_password: str, hashed_password: str)-> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str):
    return pwd_context.hash(password)

async def authenticate_user(username: str, password: str)-> User:
    user = await get_user_by_username(session=,username=username)



