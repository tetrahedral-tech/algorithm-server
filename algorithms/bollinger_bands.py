from talib import BBANDS

def algorithm(prices, window_size=20, standard_deviations=2):
	upper_band, middle_band, lower_band = BBANDS(prices, window_size, standard_deviations, standard_deviations, 0)
	return upper_band, lower_band, middle_band

def signal(prices, data):
	upper_band, lower_band, middle_band, prices = data
	if prices[-1] > upper_band[-1]:
		return 'sell', 1
	elif prices[-1] < lower_band[-1]:
		return 'buy', 0.5
	return 'no_action', 0
