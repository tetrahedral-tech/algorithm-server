from .bollinger_bands import Algorithm as BollingerBands
from .rsi import Algorithm as RSI
import matplotlib.pyplot as plt
import plots.colors as colors
from matplotlib.gridspec import GridSpec

class Algorithm:

	def __init__(self, rsi_window_size=13, bollinger_bands_window_size=20, rsi_high=70, rsi_low=30):
		self.rsi_window_size = rsi_window_size
		self.rsi_high = rsi_high
		self.rsi_low = rsi_low
		self.bollinger_bands_window_size = bollinger_bands_window_size
		self.window_size = max(rsi_window_size, bollinger_bands_window_size)

	def algorithm(self, prices):
		Bollinger_Bands = BollingerBands(window_size=self.bollinger_bands_window_size)
		bb_data = Bollinger_Bands.algorithm(prices)
		rsi = RSI(window_size=self.rsi_window_size, high=self.rsi_high, low=self.rsi_low)
		rsi_line = rsi.algorithm(prices)

		return [*bb_data, rsi_line]

	def signal(self, prices, data):
		price = prices[-1]

		upper_bands, _, lower_bands, rsi_line = data  #middle bands not needed && corrected bollinger bands from upper, lowe, middle to current
		if (lower_bands[-1] >= price) & (self.rsi_low >= rsi_line[-1]):
			return 'buy', 1

		if (upper_bands[-1] <= price) & (self.rsi_high <= rsi_line[-1]):
			return 'sell', 0.5

		return 'no_action', 0

	def plot(self, prices, timestamps, **kwargs):
		gs = GridSpec(3, 1, figure=plt.gcf())

		plt.subplot(gs[0, :])
		plt.plot(timestamps, prices, color=colors.primary())

		upper_bands, _, lower_bands, rsi_line = self.algorithm(prices, **kwargs)
		sliced_prices = prices[:min(upper_bands.shape[0], rsi_line.shape[0])]

		sell_condition = (prices >= upper_bands) & (rsi_line >= self.rsi_high)
		buy_condition = (lower_bands >= prices) & (self.rsi_low >= rsi_line)
		plt.scatter(timestamps[sell_condition], sliced_prices[sell_condition], color=colors.sell())
		plt.scatter(timestamps[buy_condition], sliced_prices[buy_condition], color=colors.buy())

		plt.subplot(gs[-1, :])
		rsi = RSI(window_size=self.rsi_window_size)
		rsi.plot(prices, timestamps, custom_algorithm_plot=True)
		plt.subplot(gs[-2, :])
		Bollinger_Bands = BollingerBands(window_size=self.bollinger_bands_window_size)
		Bollinger_Bands.plot(prices, timestamps)
