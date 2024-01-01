import matplotlib.pyplot as plt
import plots.colors as colors
from talib import BBANDS

class Algorithm:

	def __init__(self, window_size=20, standard_deviations=2):
		self.window_size, self.standard_deviations = window_size, standard_deviations

	def algorithm(self, prices):
		return BBANDS(prices,
		              timeperiod=self.window_size,
		              nbdevup=self.standard_deviations,
		              nbdevdn=self.standard_deviations)

	def signal(self, prices, data):
		upper_bands, _, lower_bands = data
		if prices[-1] > upper_bands[-1]:
			return 'sell', 1
		elif prices[-1] < lower_bands[-1]:
			return 'buy', 1

		return 'no_action', 0

	def plot(self, prices, timestamps, **kwargs):
		upper_bands, middle_bands, lower_bands = self.algorithm(prices, **kwargs)

		plt.fill_between(timestamps, upper_bands, lower_bands, color='grey', alpha=0.3)

		# Price/SMA
		plt.plot(timestamps, prices, color=colors.primary())
		plt.plot(timestamps, middle_bands, color=colors.secondary())

		# Buy/Sell Signals
		sell_condition = prices >= upper_bands
		buy_condition = prices <= lower_bands

		plt.scatter(timestamps[sell_condition], prices[sell_condition], color=colors.sell())
		plt.scatter(timestamps[buy_condition], prices[buy_condition], color=colors.buy())
