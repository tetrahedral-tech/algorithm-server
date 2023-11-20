import numpy as np
import matplotlib.pyplot as plt
import plots.colors as colors
from matplotlib.gridspec import GridSpec
from algorithms.custom_bollinger_rsi import algorithm as custom_bollinger_rsi
from plots.rsi import plot as rsi
from plots.bollinger_bands import plot as bollinger_bands

def plot(prices, **kwargs):
	gs = GridSpec(3, 1, figure=plt.gcf())

	plt.subplot(gs[0, :])
	indicies = np.arange(0, prices.shape[0])
	plt.plot(indicies, prices, color=colors.mainline())

	upper_band, lower_band, middle_band, rsi_line = custom_bollinger_rsi(prices, **kwargs)
	sliced_prices = prices[:min(upper_band.shape[0], rsi_line.shape[0])]
	indicies = np.arange(0, indicies.shape[0])

	upper_condition = (prices >= upper_band) & (rsi_line >= 70)
	lower_condition = (prices >= lower_band) & (30 >= rsi_line)
	plt.scatter(indicies[upper_condition], sliced_prices[upper_condition], color=colors.upper())
	plt.scatter(indicies[lower_condition], sliced_prices[lower_condition], color=colors.lower())

	plt.subplot(gs[-1, :])
	rsi(prices)
	plt.subplot(gs[-2, :])
	bollinger_bands(prices)

	return plt
