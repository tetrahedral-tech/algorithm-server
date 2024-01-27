import matplotlib.pyplot as plt
import plots.colors as colors
import numpy as np
from talib import MACD, EMA

class Algorithm:

	def __init__(self, fastperiod=12, slowperiod=26, signalperiod=9):
		self.fastperiod, self.slowperiod, self.signalperiod = fastperiod, slowperiod, signalperiod

	def algorithm(self, prices: list[float]) -> tuple[float]:
		return MACD(prices, fastperiod=self.fastperiod, slowperiod=self.slowperiod, signalperiod=self.signalperiod)

	def signal(self, _, data: tuple[float]):
		macds, signals, histogram = data
		positive_histogram = np.abs(histogram)
		histogram_max = np.max(np.nan_to_num(positive_histogram))

		if macds[-1] > signals[-1] and any(signal > macd for macd in macds[-5:-1] for signal in signals[-5:-1]):
			return 'buy', 1
		elif macds[-1] < signals[-1] and any(macd > signal for macd in macds[-5:-1] for signal in signals[-5:-1]):
			return 'sell', 1
		return 'no_action', 0

	def plot(self, prices: list[float], timestamps: list[float], **kwargs):
		macd, signal, histogram = self.algorithm(prices, **kwargs)

		buy_condition = np.insert((macd[1:] > signal[1:]) & (macd[:-1] < signal[:-1]), 0, False)
		sell_condition = np.insert((macd[1:] < signal[1:]) & (macd[:-1] > signal[:-1]), 0, False)

		plt.subplot(211)
		plt.plot(timestamps, prices, color=colors.primary(), label='Price')
		plt.plot(timestamps, EMA(prices, timeperiod=12), color=colors.secondary(), label='12 EMA')
		plt.plot(timestamps, EMA(prices, timeperiod=26), color=colors.tertiary(), label='26 EMA')

		plt.scatter(timestamps[buy_condition], prices[buy_condition], color=colors.buy(), label='Buy signals')
		plt.scatter(timestamps[sell_condition], prices[sell_condition], color=colors.sell(), label='Sell signals')
		plt.title("MACD-Price plots")
		plt.xlabel("Time")
		plt.ylabel("Price")

		plt.legend()

		plt.subplot(212)
		plt.plot(timestamps, macd, color=colors.primary(), label='Macd line')
		plt.plot(timestamps, signal, color=colors.secondary(), label='Signal line')

		plt.bar(timestamps[histogram >= 0], histogram[histogram >= 0], color=colors.buysecondary())
		plt.bar(timestamps[histogram < 0], histogram[histogram < 0], color=colors.sellsecondary())
		plt.plot(timestamps, np.zeros(prices.shape[0]), color=colors.inner(), linestyle='-', label='Zero Line')

		plt.scatter(timestamps[buy_condition], signal[buy_condition], color=colors.buy(), label='Buy signals')
		plt.scatter(timestamps[sell_condition], signal[sell_condition], color=colors.sell(), label='Sell signals')
		plt.title("MACD plots")
		plt.xlabel("Time")
		plt.ylabel("Price")

		plt.legend()
