from talib import MACD
import matplotlib.pyplot as plt
import plots.colors as colors

def algorithm(prices, fastperiod=12, slowperiod=26, signalperiod=9):
	return MACD(prices, fastperiod=fastperiod, slowperiod=slowperiod,
	            signalperiod=signalperiod)  #macd, macdsignal, macdhist

def signal(prices, data):
	macd, signal, hist = data
	if macd[-1] == signal[-1]:
		return 'no_action', 0

	elif macd[-2] == signal[-2]:
		if macd[-1] > signal[-1]:
			return 'buy', 0.5
		elif signal[-1] > macd[-1]:
			return 'sell', 1

	else:
		return 'no_action', 0
