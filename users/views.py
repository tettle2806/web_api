from fastapi import APIRouter

from core.models import db_helper
from users import crud
from users.auth import UserAuth
from users.schemas import UserPD, TokenGet

user_auth = UserAuth()

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/")
async def create_user(user: UserPD):
    async with db_helper.session_factory() as session:
        hash_pass = crud.hash_password(user.password)
        try:
            await crud.create_user_crud(
                username=user.username,
                email=user.email,
                session=session,
                password=hash_pass,
            )
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
            }
        return crud.create_user(user_in=user)


@router.post("/login")
async def login(user: UserPD):
    # получаем токен и возращаем клиенту
    token = user_auth.login_for_access_token(user.email, user.password)
    return token


@router.post("/me")
async def read_me(token: TokenGet):
    # декодируем токен и получаем обьект пользователя
    return user_auth.decode_token(token.token)
