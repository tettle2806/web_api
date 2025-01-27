from contextlib import asynccontextmanager


from fastapi import FastAPI, status, Request
from fastapi.params import Cookie, Depends
from fastapi.responses import RedirectResponse, HTMLResponse

from fastapi_login import LoginManager

from api_v1 import router as router_v1
import uvicorn
from core.models import Base, db_helper
from items_views import router as items_router
from users.views import router as users_router
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)

SECRET = "secret-key"

manager = LoginManager(SECRET, tokenUrl="/user/login", use_cookie=True)
manager.cookie_name = "some-name"

app.include_router(router=users_router)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)

app.include_router(router=items_router)


@app.get("/")
def hello_index():
    return {
        "message": "MAIN PAGE",
    }

@app.get('/logout', response_class=HTMLResponse)
def protected_route(request: Request, user=Depends(manager)):
    resp = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp, "")
    return resp


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
