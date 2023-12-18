from talib import BBANDS
import matplotlib.pyplot as plt
import plots.colors as colors

def algorithm(prices, window_size=20, standard_deviations=2):
	return BBANDS(prices, timeperiod=window_size, nbdevup=standard_deviations, nbdevdn=standard_deviations)

def signal(prices, data):
	upper_band, middle_band, lower_band = data

	if prices[-1] > upper_band[-1]:
		return 'sell', 1
	elif prices[-1] < lower_band[-1]:
		return 'buy', 0.5

	return 'no_action', 0

def plot(prices, timestamps, **kwargs):
	upper_band, middle_band, lower_band = algorithm(prices, **kwargs)

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
