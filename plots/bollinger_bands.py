import numpy as np
import matplotlib.pyplot as plt
from algorithms.bollinger_bands import algorithm as boillinger_bands
import plots.colors as colors

def plot(prices, timestamps, **kwargs):
	upper_band, middle_band, lower_band = boillinger_bands(prices, window_size=(20, 'days'), **kwargs)

	plt.fill_between(timestamps, upper_band, lower_band, color='grey', alpha=0.3)

	# Price/SMA
	plt.plot(timestamps, prices, color=colors.mainline())
	plt.plot(timestamps, middle_band, color=colors.secondaryline())

	# Buy/Sell Signals
	upper_condition = prices >= upper_band
	lower_condition = prices <= lower_band

	plt.scatter(timestamps[upper_condition], prices[upper_condition], color=colors.upper())
	plt.scatter(timestamps[lower_condition], prices[lower_condition], color=colors.lower())

	return plt
