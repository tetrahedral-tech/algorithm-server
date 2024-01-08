from talib import RSI
import numpy as np
import matplotlib.pyplot as plt
import plots.colors as colors
from matplotlib.gridspec import GridSpec

class Algorithm:

	def __init__(self, window_size=14, high=70, low=30):
		self.window_size = window_size
		self.high = high
		self.low = low

	def algorithm(self, prices):
		return RSI(prices, timeperiod=self.window_size)

	def signal(self, _, data):
		rsi = data

		if rsi[-1] > self.high:
			strength = (rsi[-1] - self.high) * (1 / self.low)
			return 'sell', strength
		elif rsi[-1] < self.low:
			strength = 1 - rsi[-1] * (1 / self.low)
			return 'buy', strength

		return 'no_action', 0

	def plot(self, prices, timestamps, **kwargs):
		gs = GridSpec(3, 1, figure=plt.gcf())

		plt.subplot(gs[0, :])
		rsi_line = self.algorithm(prices, **kwargs)

		plt.plot(timestamps, rsi_line, color=colors.primary(), label='RSI')

		# Thresholds
		upper = np.full(rsi_line.shape, self.high)
		lower = np.full(rsi_line.shape, self.low)
		sell_condition = rsi_line >= self.high
		buy_condition = rsi_line <= self.low

		plt.fill_between(timestamps, upper, lower, color='grey', alpha=0.3)
		plt.plot(timestamps, upper, linestyle='dashed', color=colors.sell(), label='RSI high band')
		plt.plot(timestamps, lower, linestyle='dashed', color=colors.buy(), label='RSI low band')
		plt.title("RSI Plots")
		plt.xlabel("Time")
		plt.ylabel("RSI LINE")
		plt.legend()

		plt.subplot(gs[1, :])
		plt.plot(timestamps, prices, color=colors.primary(), label='price')
		plt.scatter(timestamps[sell_condition], prices[sell_condition], color=colors.sell(), label='Sell conditions')
		plt.scatter(timestamps[buy_condition], prices[buy_condition], color=colors.buy(), label='Buy conditions')
		plt.title("Time-signals")
		plt.xlabel("Time")
		plt.ylabel("Price")
		plt.legend()