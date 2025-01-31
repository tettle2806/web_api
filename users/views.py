from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.models import db_helper
from users import crud
from users.auth import authenticate_user, create_access_token
from users.schemas import CreateUser, Token

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/")
async def create_user(user: CreateUser):
    async with db_helper.session_factory() as session:
        hash_pass = crud.hash_password(user.password)
        await crud.create_user_crud(
            username=user.username,
            email=user.email,
            session=session,
            password=hash_pass,
        )
        return crud.create_user(user_in=user)


@router.get("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
