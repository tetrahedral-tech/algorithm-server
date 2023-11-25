import numpy as np
import matplotlib.pyplot as plt
import plots.colors as colors
from algorithms.rsi import algorithm as rsi

def plot(prices, timestamps, **kwargs):
	rsi_line = rsi(prices, **kwargs)

	plt.plot(timestamps, rsi_line, color=colors.mainline())

	# Thresholds
	upper = np.full(rsi_line.shape, 70)
	lower = np.full(rsi_line.shape, 30)

	plt.fill_between(timestamps, upper, lower, color='grey', alpha=0.3)
	plt.plot(timestamps, upper, linestyle='dashed', color=colors.upper())
	plt.plot(timestamps, lower, linestyle='dashed', color=colors.lower())

	return plt
