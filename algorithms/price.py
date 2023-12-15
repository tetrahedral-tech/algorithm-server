import numpy as np
import matplotlib.pyplot as plt
import plots.colors as colors

def plot(prices, timestamps):
	plt.plot(timestamps, prices, color=colors.primary())

	return plt
