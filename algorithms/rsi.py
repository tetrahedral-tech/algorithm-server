from talib import RSI
from price import get_periods, get_max_periods

def algorithm(prices, window_size=(14, 'days')):
	periods = get_periods(*window_size)

	if get_max_periods() < periods:
		raise Exception(f'Not Enough Datapoints for this Interval')

	return RSI(prices, timeperiod=get_periods(*window_size))

def signal(prices, data, high=70, low=30):
	rsi = data
	if rsi[-1] > high:
		strength = (rsi[-1] - high) * (1 / low)
		return 'sell', strength
	elif rsi[-1] < low:
		strength = 1 - rsi[-1] * (1 / low)
		return 'buy', strength
	return 'no_action', 0
