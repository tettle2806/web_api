import asyncio
import logging
import sys
from contextlib import asynccontextmanager


from fastapi import FastAPI
from starlette.responses import RedirectResponse

from api_v1 import router as router_v1
import uvicorn
from core.models import Base, db_helper
from items_views import router as items_router
from telegram_bot.run import main
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


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
