import requests


async def binance_ticker_price(ticker: str) -> dict:
    r = requests.get(f'https://data-api.binance.vision/api/v3/ticker/price?symbol={ticker}')
    return r.json()

async def binance_avg_price(ticker: str) -> dict:
    r = requests.get(f'https://data-api.binance.vision/api/v3/avgPrice?symbol={ticker}')
    return r.json()







