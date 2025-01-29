from fastapi import APIRouter
from starlette.responses import JSONResponse

from blockchains_api.bitcoin_api import (
    binance_ticker_price,
    binance_avg_price,
    binance_exchange_info,
    binance_ticker_info,
    binance_ticker24_info,
)

router = APIRouter(
    prefix="/crypto",
    tags=["Crypto"],
)


@router.get("/price")
async def crypto_price(ticker: str) -> dict:
    logs = await binance_ticker_price(ticker)
    return logs


@router.get("/avg_price")
async def avg_price(ticker: str) -> dict:
    logs = await binance_avg_price(ticker)
    return logs


@router.get("/exchangeInfo")
async def exchange_info(ticker: str) -> dict:
    logs = await binance_exchange_info(ticker)
    return logs


@router.get("/tickerInfo")
async def ticker_info(ticker: str) -> dict:
    logs = await binance_ticker_info(ticker)
    return logs


@router.get("/tickerInfo24hr")
async def ticker_info24hr(ticker: str) -> dict:
    logs = await binance_ticker24_info(ticker)
    return logs
