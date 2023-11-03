import numpy as np
import matplotlib.pyplot as plt
import plots.colors as colors

def plot(prices):
	indicies = np.arange(0, prices.shape[0])
	plt.plot(indicies, prices, color=colors.mainline())

	return plt
