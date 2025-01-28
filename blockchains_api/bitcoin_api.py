# Simple python websocket client
# https://github.com/websocket-client/websocket-client
from websocket import create_connection
options = {'symbols': 'BTC-USD', 'channels': 'trades', 'prices': 'spot'}
api_key = '1fb82035-6fb4-4b61-896c-22bb631d18e4'
options['origin'] = 'https://exchange.blockchain.com'
url = "wss://ws.blockchain.info/mercury-gateway/v1/ws"
ws = create_connection(url, **options)
msg = '{"token": "{eyJhbGciOiJFUzI1NiIsInR5cCI6IkFQSSJ9.eyJpc3MiOiJibG9ja2NoYWluIiwiYXVkIjoibWVyY3VyeSIsImlhdCI6MTczODA2MTY5NiwianRpIjoiMWZiODIwMzUtNmZiNC00YjYxLTg5NmMtMjJiYjYzMWQxOGU0IiwidWlkIjoiZWZkOTM2NWUtYWQ5NS00YzdmLWI2MmUtNDA4YTM3ZTRhZWUxIiwic2VxIjo4MjQwNTk2LCJyZG8iOnRydWUsIndkbCI6ZmFsc2V9.IB/+pDzQCV+81Ao3vxJBEYw39OgORzhDxIDi7wSzPXlCXbya3N906fwAxZ51HDzJxBqyKwCJmrmbolw9EXR1YKc=}", "action": "subscribe", "channel": "prices"}'
ws.send(msg)
result =  ws.recv()
print(result)
# { "seqnum":0,
#   "event":"subscribed",
#   "channel":"auth",
#   "readOnly":false }
ws.close()
