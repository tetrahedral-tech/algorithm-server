import numpy as np
import matplotlib.pyplot as plt

def plot(bot_profit):
	bot_profit = np.array(bot_profit)
	indicies = np.arange(0, bot_profit.shape[0]) * 5
	plt.plot(indicies, bot_profit, color='lightcoral')

	return plt