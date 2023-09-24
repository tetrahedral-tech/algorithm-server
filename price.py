import numpy as np
from requests import get

def get_prices(pair, interval=15):
	ohlc = get(f'https://api.kraken.com/0/public/OHLC?pair={pair}&interval={interval}').json()
	ticker = get(f'https://api.kraken.com/0/public/Ticker?pair={pair}').json()

	current = float(list(ticker['result'].values())[0]['c'][0])
	prices = [float(point[4]) for point in list(ohlc['result'].values())[0]]

	return np.array([current, *prices])
