
from contextlib import asynccontextmanager


from fastapi import FastAPI
from fastapi.security import HTTPBasic


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


app.include_router(router=users_router)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)

app.include_router(router=items_router)



@app.get("/")
def hello_index():
    return {
        "message": "MAIN PAGE",
    }

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
