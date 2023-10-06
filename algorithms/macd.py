from talib import MACD

def algorithm(prices, window_sizes=[12, 26, 9]):
	macd, signal, hist = MACD(prices, window_sizes[0], window_sizes[1], signalperiod=window_sizes[2])
	return macd, signal

def signal(data):
	macd, signal = data
	if macd[-1] > signal[-1]:
		return 'sell'
	elif macd[-1] < signal[-1]:
		return 'buy'
	return 'no_action'
