import numpy as np
import matplotlib.pyplot as plt
from algorithms.rsi import algorithm as rsi
import plots.colors as colors

def plot(prices):
	rsi_line = rsi(prices)
	indicies = np.arange(0, rsi_line.shape[0])

	plt.plot(indicies, rsi_line, color=colors.mainline())

	# Thresholds
	upper = np.full(rsi_line.shape, 70)
	lower = np.full(rsi_line.shape, 30)

	plt.fill_between(indicies, upper, lower, color='grey', alpha=0.3)
	plt.plot(indicies, upper, linestyle='dashed', color=colors.upper())
	plt.plot(indicies, lower, linestyle='dashed', color=colors.lower())

	return plt
