import numpy as np
import matplotlib.pyplot as plt
from algorithms.bollinger_bands import algorithm as boillinger_bands
import plots.colors as colors

def plot(prices, **kwargs):
	upper_band, lower_band, middle_band = boillinger_bands(prices, **kwargs)

	indicies = np.arange(0, upper_band.shape[0])
	sliced_prices = prices[:upper_band.shape[0]]

	plt.fill_between(indicies, upper_band, lower_band, color='grey', alpha=0.3)

	# Price/SMA
	plt.plot(indicies, sliced_prices, color=colors.mainline())
	plt.plot(indicies, middle_band, color=colors.secondaryline())

	# Buy/Sell Signals
	upper_condition = sliced_prices >= upper_band
	lower_condition = sliced_prices <= lower_band

	plt.scatter(indicies[upper_condition], sliced_prices[upper_condition], color=colors.upper())
	plt.scatter(indicies[lower_condition], sliced_prices[lower_condition], color=colors.lower())

	return plt
