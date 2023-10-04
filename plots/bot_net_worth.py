import numpy as np
import matplotlib.pyplot as plt
import plots.colors as colors

def plot(bot_profit):
	bot_profit = np.array(bot_profit)
	indicies = np.arange(0, bot_profit.shape[0]) * 5
	plt.plot(indicies, bot_profit, color=colors.upper())

	return plt
