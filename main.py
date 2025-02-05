from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from api_v1 import router as router_v1
import uvicorn
from core.models import db_helper
from exeptions import TokenExpiredException, TokenNoFoundException
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


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Разрешить запросы с любых источников. Можете ограничить список доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

app.include_router(router=users_router)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)

app.include_router(router=items_router)
app.include_router(router=blockchain_router)


@app.get("/")
async def get():
    return {"message": "Hello"}


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


@app.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(request: Request, exc: HTTPException):
    # Возвращаем редирект на страницу /auth
    return RedirectResponse(url="/auth")


# Обработчик для TokenNoFound
@app.exception_handler(TokenNoFoundException)
async def token_no_found_exception_handler(request: Request, exc: HTTPException):
    # Возвращаем редирект на страницу /auth
    return RedirectResponse(url="/auth")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
