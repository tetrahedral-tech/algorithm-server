from talib import BBANDS
from price import get_periods

def algorithm(prices, window_size=(20, 'days'), standard_deviations=2):
	print(prices.shape[0])
	print(get_periods(*window_size))
	return BBANDS(prices, timeperiod=get_periods(*window_size), nbdevup=standard_deviations, nbdevdn=standard_deviations)

def signal(prices, data):
	upper_band, middle_band, lower_band = data
	if prices[-1] > upper_band[-1]:
		return 'sell', 1
	elif prices[-1] < lower_band[-1]:
		return 'buy', 0.5
	return 'no_action', 0
