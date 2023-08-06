# binanceus-python
A lightweight Python wrapper for the binance.us public API. 

Uses [binance-connector-python](https://github.com/binance/binance-connector-python) for API connectivity.

I am in no way affiliated with Binance or Binance US. Use this at your own risk.

## Quick Start
Install binanceus-python: `pip install binanceus-python` 

Here's some example code to get started with:

```python
from websocket_bs.client import BsWebsocketClient
import time

# start real-time ticker stream for symbol BTCUSD
symbol = 'BTCUSD'

ws = BsWebsocketClient()
ws.subscribe(symbol)
ws.start()


# print live ticker feed
try:
    while True:
        book_top = ws.get_book_top(symbol)
        bid = book_top[0]
        bid_qty = book_top[1]
        ask = book_top[2]
        ask_qty = book_top[3]
        print(f'{symbol} SPOT orderbook_top: ({bid:0.4f}, {bid_qty})  ({ask:0.4f}, {ask_qty})')
        time.sleep(1)
except KeyboardInterrupt as e:
    print("Program finished.")
    ws.stop()
```

## Contributing 
Contributions, fixes, recommendations, and all other feedback is welcome. If you are fixing a bug, please open an issue first with all relevant details, and mention the issue number in the pull request.

### Contact 
I can be reached on discord at Nenye#5335, or through email at nenye@ndili.net. Otherwise, feel free to open a PR or Issue here.
