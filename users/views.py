from uuid import uuid4

from fastapi import APIRouter, HTTPException, Depends, status

from core.models import db_helper
from users.crud import get_user_by_email, create_user_crud
from users.deps import get_current_user
from users.schemas import UserOut, UserAuth, SystemUser
from users.utils import (
    get_hashed_password,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
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


@router.get(
    "/me", summary="Get details of currently logged in user", response_model=UserOut
)
async def get_me(user: SystemUser = Depends(get_current_user)):
    return user
