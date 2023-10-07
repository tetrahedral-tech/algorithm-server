from talib import RSI

def algorithm(prices, window_size=14):
	return RSI(prices, window_size)

def signal(prices, data, high=70, low=30):
	rsi = data
	if rsi[-1] > high:
		return 'sell'
	elif rsi[-1] < low:
		return 'buy'
	return 'no_action'
