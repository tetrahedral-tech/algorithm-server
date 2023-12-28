from .bollinger_bands import Algorithm as BB_algorithm
from .rsi import Algorithm as RSI_algorithm
import matplotlib.pyplot as plt
import plots.colors as colors
from matplotlib.gridspec import GridSpec

class Algorithm:
	def __init__(self, rsi_window_size=13, bollinger_bands_window_size=30):
		self.rsi_window_size = rsi_window_size
		self.bollinger_bands_window_size = bollinger_bands_window_size
		self.window_size = max(rsi_window_size, bollinger_bands_window_size)

	def algorithm(self, prices):
		Bollinger_Bands = BB_algorithm(window_size=self.bollinger_bands_window_size)
		bb_data = Bollinger_Bands.algorithm(prices)
		RSI = RSI_algorithm(window_size=self.rsi_window_size)
		rsi_line = RSI.algorithm(prices)

		return [*bb_data, rsi_line]

	def signal(self, prices, data):
		price = prices[-1]
		upper_bands, _, lower_bands, rsi_line = data #middle bands not needed && corrected bollinger bands from upper, lowe, middle to current
		if (lower_bands[-1] >= price) & (30 >= rsi_line[-1]):
			return 'buy', 1

		if (upper_bands[-1] <= price) & (70 <= rsi_line[-1]):
			return 'sell', 0.5

		return 'no_action', 0

	def plot(self, prices, timestamps, **kwargs):
		gs = GridSpec(3, 1, figure=plt.gcf())

		plt.subplot(gs[0, :])
		plt.plot(timestamps, prices, color=colors.primary())

		upper_bands, _, lower_bands, rsi_line = self.algorithm(prices, **kwargs)
		sliced_prices = prices[:min(upper_bands.shape[0], rsi_line.shape[0])]

		upper_condition = (prices >= upper_bands) & (rsi_line >= 70)
		lower_condition = (lower_bands >= prices) & (30 >= rsi_line)
		plt.scatter(timestamps[upper_condition], sliced_prices[upper_condition], color=colors.upper())
		plt.scatter(timestamps[lower_condition], sliced_prices[lower_condition], color=colors.lower())

		plt.subplot(gs[-1, :])
		RSI = RSI = RSI_algorithm(window_size=self.rsi_window_size)
		RSI.plot(prices, timestamps)
		plt.subplot(gs[-2, :])
		Bollinger_Bands = BB_algorithm(window_size=self.bollinger_bands_window_size)
		Bollinger_Bands.plot(prices, timestamps)
