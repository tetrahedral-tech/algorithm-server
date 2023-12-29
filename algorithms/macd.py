import matplotlib.pyplot as plt
import plots.colors as colors
import numpy as np
from talib import MACD, EMA

class Algorithm:

	def __init__(self, fastperiod=12, slowperiod=26, signalperiod=9):
		self.fastperiod, self.slowperiod, self.signalperiod = fastperiod, slowperiod, signalperiod

	def algorithm(self, prices):
		return MACD(prices, fastperiod=self.fastperiod, slowperiod=self.slowperiod, signalperiod=self.signalperiod)

	def signal(self, _, data):
		macd, signal, histogram = data
		positive_histogram = np.abs(histogram)
		histogram_max = np.max(np.nan_to_num(positive_histogram))

		if macd[-1] > signal[-1] and macd[-2] < signal[-2]:
			return 'buy', positive_histogram[-1] / histogram_max
		elif macd[-1] < signal[-1] and macd[-2] > signal[-2]:
			return 'sell', positive_histogram[-1] / histogram_max

		return 'no_action', 0

	def plot(self, prices, timestamps, **kwargs):
		macd, signal, histogram = self.algorithm(prices, **kwargs)

		upper_condition = np.insert((macd[1:] > signal[1:]) & (macd[:-1] < signal[:-1]), 0, False)
		lower_condition = np.insert((macd[1:] < signal[1:]) & (macd[:-1] > signal[:-1]), 0, False)

		plt.subplot(211)
		plt.plot(timestamps, prices, color=colors.primary())
		plt.plot(timestamps, EMA(prices, timeperiod=12), color=colors.secondary())
		plt.plot(timestamps, EMA(prices, timeperiod=26), color=colors.tertiary())

		plt.scatter(timestamps[upper_condition], prices[upper_condition], color=colors.upper())
		plt.scatter(timestamps[lower_condition], prices[lower_condition], color=colors.lower())

		plt.subplot(212)
		plt.plot(timestamps, macd, color=colors.primary())
		plt.plot(timestamps, signal, color=colors.secondary())

		plt.bar(timestamps[histogram >= 0], histogram[histogram >= 0], color=colors.uppersecondary())
		plt.bar(timestamps[histogram < 0], histogram[histogram < 0], color=colors.lowersecondary())
		plt.plot(timestamps, np.zeros(prices.shape[0]), color=colors.inner(), linestyle='-')

		plt.scatter(timestamps[upper_condition], signal[upper_condition], color=colors.upper())
		plt.scatter(timestamps[lower_condition], signal[lower_condition], color=colors.lower())
