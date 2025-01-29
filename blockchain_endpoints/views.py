from fastapi import APIRouter
from starlette.responses import JSONResponse

from blockchains_api.bitcoin_api import binance_ticker_price, binance_avg_price, exchange_info

router = APIRouter(
    prefix="/crypto",
    tags=["Crypto"],
)


@router.get("/price")
async def crypto_price(ticker: str)-> JSONResponse:
    logs = await binance_ticker_price(ticker)
    return logs

@router.get("/avg_price")
async def avg_price(ticker: str)-> JSONResponse:
    logs = await binance_avg_price(ticker)
    return logs

@router.get("/exchangeInfo")
async def avg_price(ticker: str)-> JSONResponse:
    logs = await exchange_info(ticker)
    return logs
