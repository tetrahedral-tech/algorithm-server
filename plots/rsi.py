import numpy as np
import matplotlib.pyplot as plt
from algorithms.rsi import algorithm as rsi
import colors

def plot(prices):
	rsi_data = rsi(prices)
	rsi_indicies = np.arange(0, rsi_data.shape[0])

	plt.plot(rsi_indicies, rsi_data, color=colors.mainline())

	# Thresholds
	rsi_upper = np.full(rsi_data.shape, 70)
	rsi_lower = np.full(rsi_data.shape, 30)

	plt.fill_between(rsi_indicies, rsi_upper, rsi_lower, color='grey', alpha=0.3)
	plt.plot(rsi_indicies, rsi_upper, linestyle='dashed', color=colors.upper())
	plt.plot(rsi_indicies, rsi_lower, linestyle='dashed', color=colors.lower())

	return plt
