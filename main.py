import secrets
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Cookie, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession


from api_v1 import router as router_v1
import uvicorn
from core.models import Base, db_helper
from items_views import router as items_router
from users.views import router as users_router
from core.config import settings
from users.crud import get_user_by_username, hash_password

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)
security = HTTPBasic()

app.include_router(router=router_v1, prefix=settings.api_v1_prefix)

app.include_router(router=items_router)
app.include_router(router=users_router)


@app.get("/")
def hello_index():
    return {
        "message": "MAIN PAGE",
    }


async def get_current_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)], session: AsyncSession
):

    current_username_bytes = credentials.username.encode("utf8")
    async with db_helper.session_factory() as session:
        correct_username_bytes = await get_user_by_username(username=credentials.username, session=session)
        correct_password_bytes = await get_user_by_username(username=credentials.username, session=session)
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes.username.encode("utf8")
    )
    current_password_bytes = hash_password(credentials.password.encode("utf8")).encode("utf8")

    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes.password.encode("utf8")
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@users_router.get("/me")
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(get_current_username)]):
    return {"username": credentials.username, "password": credentials.password}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
