from fastapi import APIRouter
from hashlib import sha256
import hmac

from core.models import db_helper
from users import crud
from users.schemas import CreateUser
router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/")
async def create_user(user: CreateUser):
    async with db_helper.session_factory() as session:
        hash_pass = crud.hash_password(user.password)
        await crud.create_user_crud(username=user.username, email=user.email, session=session, password=hash_pass)
        return crud.create_user(user_in=user)
