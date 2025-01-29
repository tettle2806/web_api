from fastapi import APIRouter
from starlette.responses import JSONResponse

from blockchains_api.bitcoin_api import binance_ticker_prices

router = APIRouter(
    prefix="/crypto",
    tags=["Crypto"],
)


@router.get("price")
async def crypto_price(ticker: str)-> JSONResponse:
    logs = await binance_ticker_prices(ticker)
    return logs