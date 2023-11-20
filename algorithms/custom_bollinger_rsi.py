from .bollinger_bands import algorithm as bollinger_bands
from .rsi import algorithm as rsi

def algorithm(prices, window_size_rsi=13, window_size_bollinger_bands=30):
	upper_band, lower_band, middle_band = bollinger_bands(prices, window_size=window_size_bollinger_bands)
	rsi_line = rsi(prices, window_size=window_size_rsi)

	return upper_band, lower_band, middle_band, rsi_line

def signal(prices, data):
	price = prices[-1]
	upper_band, lower_band, middle_band, rsi_line = data

	if price >= lower_band[-1] and 30 >= rsi_line[-1]:
		return 'buy', 0.5

	if price >= upper_band[-1] and rsi_line[-1] >= 70:
		return 'sell', 1
