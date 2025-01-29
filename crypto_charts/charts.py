import matplotlib.pyplot as plt

import ccxt
import pandas as pd

exchange = ccxt.binance()
print(exchange)
symbol = 'BTC/USDT'
timeframe = '1d'

ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

print(df.head())

plt.plot(df['timestamp'], df['close'])
plt.xlabel('Дата')
plt.ylabel('Цена закрытия')
plt.title('График цены закрытия BTC/USDT')
plt.show()