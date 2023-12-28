import matplotlib.pyplot as plt
import plots.colors as colors

class Algorithm:
	def plot(prices, timestamps):
		plt.plot(timestamps, prices, color=colors.primary())
		return plt
