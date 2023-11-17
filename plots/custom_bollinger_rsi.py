import numpy as np
import matplotlib.pyplot as plt
from plots.bollinger_bands import plot as bollinger_bands
from plots.rsi import plot as rsi
import plots.colors as colors

def plot(prices):
	plt.subplot(211)
	bollinger_bands(prices)

	plt.subplot(212)
	rsi(prices)
	return plt
