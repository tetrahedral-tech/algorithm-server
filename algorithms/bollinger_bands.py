from talib import BBANDS
from price import get_periods, get_max_periods

def algorithm(prices, window_size=(20, 'days'), standard_deviations=2):
	periods = get_periods(*window_size)

	if get_max_periods() < periods:
		raise Exception(f'Not Enough Datapoints for this Interval')

	return BBANDS(prices, timeperiod=periods, nbdevup=standard_deviations, nbdevdn=standard_deviations)

def signal(prices, data):
	upper_band, middle_band, lower_band = data

	if prices[-1] > upper_band[-1]:
		return 'sell', 1
	elif prices[-1] < lower_band[-1]:
		return 'buy', 0.5

	return 'no_action', 0
