import numpy as np
import matplotlib.pyplot as plt
from algorithms.macd import algorithm as macd

def plot(prices):
	macd_line, signal_line = macd(prices)
	indicies = np.arange(0, macd_line.shape[0])

	upper_condition = macd_line > signal_line
	lower_condition = macd_line < signal_line

	plt.scatter(indicies[upper_condition], signal_line[upper_condition], color='darkturquoise')
	plt.scatter(indicies[lower_condition], signal_line[lower_condition], color='lightcoral')

	plt.plot(signal_line, color='plum')
	plt.plot(macd_line, color='mediumpurple')

	return plt
