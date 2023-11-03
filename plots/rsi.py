import numpy as np
import matplotlib.pyplot as plt
from algorithms.rsi import algorithm as rsi
import plots.colors as colors

def plot(prices):
	data = rsi(prices)
	indicies = np.arange(0, data.shape[0])

	plt.plot(indicies, data, color=colors.mainline())

	# Thresholds
	upper = np.full(data.shape, 70)
	lower = np.full(data.shape, 30)

	plt.fill_between(indicies, upper, lower, color='grey', alpha=0.3)
	plt.plot(indicies, upper, linestyle='dashed', color=colors.upper())
	plt.plot(indicies, lower, linestyle='dashed', color=colors.lower())

	return plt
