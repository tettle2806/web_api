import requests


async def binance_ticker_price(ticker: str) -> dict:
    try:
        r = requests.get(
            f"https://data-api.binance.vision/api/v3/ticker/price?symbol={ticker}"
        )
        return r.json()
    except Exception as e:
        return {"error": str(e)}


async def binance_avg_price(ticker: str) -> dict:
    try:
        r = requests.get(
            f"https://data-api.binance.vision/api/v3/avgPrice?symbol={ticker}"
        )
        return r.json()
    except Exception as e:
        return {"error": str(e)}


async def binance_exchange_info(ticker: str) -> dict:
    try:
        r = requests.get(
            f"https://data-api.binance.vision/api/v3/exchangeInfo?symbol={ticker}"
        )
        return r.json()
    except Exception as e:
        return {"error": str(e)}


async def binance_ticker_info(ticker: str) -> dict:
    try:
        r = requests.get(
            f"https://data-api.binance.vision/api/v3/ticker?symbol={ticker}"
        )
        return r.json()
    except Exception as e:
        return {"error": str(e)}


async def binance_ticker24_info(ticker: str) -> dict:
    try:
        r = requests.get(
            f"https://data-api.binance.vision/api/v3/ticker/24hr?symbol={ticker}"
        )
        return r.json()
    except Exception as e:
        return {"error": str(e)}


async def binance_book_ticker(ticker: str) -> dict:
    try:
        r = requests.get(
            f"https://data-api.binance.vision/api/v3/ticker/bookTicker?symbol={ticker}"
        )
        return r.json()
    except Exception as e:
        return {"error": str(e)}
