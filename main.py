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
from blockchains_api.bitcoin_api import binance_ticker_prices

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


@app.get("/")
def hello_index():
    return {
        "message": "MAIN PAGE",
    }

@app.get("/cryptoprice")
async def crypto_price(ticker: str):
    logs = await binance_ticker_prices(ticker)
    return logs




if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
