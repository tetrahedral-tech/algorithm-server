from talib import RSI
import numpy as np
import matplotlib.pyplot as plt
import plots.colors as colors

def algorithm(prices, window_size=14):
	return RSI(prices, timeperiod=window_size)

def signal(prices, data, high=70, low=30):
	rsi = data

	if rsi[-1] > high:
		strength = (rsi[-1] - high) * (1 / low)
		return 'sell', strength

	elif rsi[-1] < low:
		strength = 1 - rsi[-1] * (1 / low)
		return 'buy', strength

	return 'no_action', 0

def plot(prices, timestamps, **kwargs):
	rsi_line = algorithm(prices, **kwargs)

	plt.plot(timestamps, rsi_line, color=colors.mainline())

	# Thresholds
	upper = np.full(rsi_line.shape, 70)
	lower = np.full(rsi_line.shape, 30)

	plt.fill_between(timestamps, upper, lower, color='grey', alpha=0.3)
	plt.plot(timestamps, upper, linestyle='dashed', color=colors.upper())
	plt.plot(timestamps, lower, linestyle='dashed', color=colors.lower())

	return plt
