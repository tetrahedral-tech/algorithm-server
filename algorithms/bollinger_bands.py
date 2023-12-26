import matplotlib.pyplot as plt
import plots.colors as colors
from talib import BBANDS

def algorithm(prices, window_size=20, standard_deviations=2):
	return BBANDS(prices, timeperiod=window_size, nbdevup=standard_deviations, nbdevdn=standard_deviations)

def signal(prices, data):
	upper_bands, _, lower_bands = data # _ because the middle band will not be used 
	if prices[-1] > upper_bands[-1]:
		return 'sell', 1
	elif prices[-1] < lower_bands[-1]:
		return 'buy', 1

	return 'no_action', 0

def plot(prices, timestamps, **kwargs):
	upper_bands, middle_bands, lower_bands = algorithm(prices, **kwargs)

	plt.fill_between(timestamps, upper_bands, lower_bands, color='grey', alpha=0.3)

	# Price/SMA
	plt.plot(timestamps, prices, color=colors.primary())
	plt.plot(timestamps, middle_bands, color=colors.secondary())

	# Buy/Sell Signals
	upper_condition = prices >= upper_bands
	lower_condition = prices <= lower_bands

	plt.scatter(timestamps[upper_condition], prices[upper_condition], color=colors.upper())
	plt.scatter(timestamps[lower_condition], prices[lower_condition], color=colors.lower())

	return plt
