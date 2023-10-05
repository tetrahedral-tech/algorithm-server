import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

def algorithm(prices, window_size=14):
	diff = np.diff(prices, 1)

	gains = np.zeros(diff.shape)
	losses = np.zeros(diff.shape)

	gains[diff > 0] = diff[diff > 0]
	losses[diff < 0] = diff[diff < 0]

	avg_gains = sliding_window_view(gains, window_size).mean(axis=-1)
	avg_losses = np.abs(sliding_window_view(losses, window_size).mean(axis=-1))

	rsi = 100 * avg_gains / (avg_gains + avg_losses)
	return rsi

def signal(data):
	rsi = data
	if rsi[-1] > 70:
		return 'sell'
	elif rsi[-1] < 30:
		return 'buy'
	return 'no_action'
