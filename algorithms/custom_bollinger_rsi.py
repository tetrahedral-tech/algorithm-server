from .bollinger_bands import algorithm as bollinger_bands
from .rsi import algorithm as rsi
import matplotlib.pyplot as plt
import plots.colors as colors
from matplotlib.gridspec import GridSpec
from algorithms.rsi import plot as rsi_plot
from algorithms.bollinger_bands import plot as bollinger_bands_plot

def algorithm(prices, window_size_rsi=13, window_size_bollinger_bands=30):
	bb_data = bollinger_bands(prices, window_size=window_size_bollinger_bands)
	rsi_line = rsi(prices, window_size=window_size_rsi)

	return [*bb_data, rsi_line]

def signal(prices, data):
	price = prices[-1]
	upper_band, lower_band, middle_band, rsi_line = data

	if lower_band[-1] >= price and 30 >= rsi_line[-1]:
		return 'buy', 1

	if price >= upper_band[-1] and rsi_line[-1] >= 70:
		return 'sell', 1

	return 'no_action', 0

def plot(prices, timestamps, **kwargs):
	gs = GridSpec(3, 1, figure=plt.gcf())

	plt.subplot(gs[0, :])
	plt.plot(timestamps, prices, color=colors.primary())

	upper_band, middle_band, lower_band, rsi_line = algorithm(prices, **kwargs)
	sliced_prices = prices[:min(upper_band.shape[0], rsi_line.shape[0])]

	upper_condition = (prices >= upper_band) & (rsi_line >= 70)
	lower_condition = (lower_band >= prices) & (30 >= rsi_line)
	plt.scatter(timestamps[upper_condition], sliced_prices[upper_condition], color=colors.upper())
	plt.scatter(timestamps[lower_condition], sliced_prices[lower_condition], color=colors.lower())

	plt.subplot(gs[-1, :])
	rsi_plot(prices, timestamps)
	plt.subplot(gs[-2, :])
	bollinger_bands_plot(prices, timestamps)

	return plt
