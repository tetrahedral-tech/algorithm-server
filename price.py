import numpy as np
from requests import get

# {60 300 900  3600   21600  86400}
#  1m 5m  15m  1h     6h     1d
#  5h 25h 3d3h 12d12h 2mo15d 10mo
def get_prices(pair, interval=21600):
	ohlc = get(f'https://api.exchange.coinbase.com/products/{pair}/candles?granularity={interval}').json()
	ticker = get(f'https://api.exchange.coinbase.com/products/{pair}/ticker').json()

	current = float(ticker['price'])
	prices = [point[4] for point in ohlc]

	return np.flip([current, *prices])
