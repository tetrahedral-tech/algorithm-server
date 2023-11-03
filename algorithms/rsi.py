from talib import RSI

def algorithm(prices, window_size=14):
	return RSI(prices, window_size)

def signal(prices, data, high=70, low=30):
	rsi = data
	if rsi[-1] > high:
		return 'sell', 0.5
	elif rsi[-1] < low:
		return 'buy', 0.5
	return 'no_action', 0
