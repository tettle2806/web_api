import asyncio
import logging
import sys
from contextlib import asynccontextmanager


from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse

from api_v1 import router as router_v1
import uvicorn
from core.models import Base, db_helper
from items_views import router as items_router
from users.crud import get_user_by_username
from users.schemas import TokenSchema
from users.utils import (
    get_hashed_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from users.views import router as users_router
from core.config import settings

from blockchain_endpoints.views import router as blockchain_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)

SECRET = "secret-key"


app.include_router(router=users_router)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)

app.include_router(router=items_router)
app.include_router(router=blockchain_router)


@app.get("/")
def hello_index():
    return RedirectResponse(url="/docs")


@app.post(
    "/login",
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema,
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    async with db_helper.session_factory() as session:
        user = await get_user_by_username(session=session, username=form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    hashed_pass = user.password
    db_hash_password = get_hashed_password(form_data.password)
    if not verify_password(db_hash_password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    return {
        "access_token": create_access_token(uuid=user.uuid, subject=user.email),
        "refresh_token": create_refresh_token(uuid=user.uuid, subject=user.email),
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
