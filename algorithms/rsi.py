from talib import RSI

def algorithm(prices, window_size=14):
	rsi = RSI(prices, window_size)
	return rsi

def signal(data):
	rsi = data
	if rsi[-1] > 70:
		return 'sell'
	elif rsi[-1] < 30:
		return 'buy'
	return 'no_action'
