from uuid import uuid4

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import Response

from core.models import db_helper
from exeptions import IncorrectEmailOrPasswordException
from users.crud import get_user_by_email, create_user_crud, get_user_by_username
from users.deps import get_current_user, reuseable_oauth
from users.schemas import UserOut, UserAuth, SystemUser, TokenSchema
from users.utils import (
    get_hashed_password, verify_password, create_access_token, create_refresh_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/signup", summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    # querying database to check if user already exist
    async with db_helper.session_factory() as session:
        user = await get_user_by_email(session=session, email=data.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist",
        )
    user = {
        "email": data.email,
        "password": get_hashed_password(data.password),
        "uuid": uuid4(),
    }
    async with db_helper.session_factory() as session:
        await create_user_crud(
            session=session,
            username=data.username,
            email=data.email,
            password=get_hashed_password(data.password),
            uuid=user["uuid"],
        )  # saving user to database
    return user


@router.post(
    "/login",
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema,
)
async def login(response:Response ,form_data: OAuth2PasswordRequestForm = Depends()):
    async with db_helper.session_factory() as session:
        user = await get_user_by_username(session=session, username=form_data.username)
    if user is None:
        raise IncorrectEmailOrPasswordException
    hashed_pass = user.password
    db_hash_password = get_hashed_password(form_data.password)
    if not verify_password(db_hash_password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(uuid=user.uuid, subject=user.email)
    refresh_token = create_refresh_token(uuid=user.uuid, subject=user.email)
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}



@router.get(
    "/me", summary="Get details of currently logged in user", response_model=UserOut
)
async def get_me(user: SystemUser = Depends(get_current_user)):
    return user
