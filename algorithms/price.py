import matplotlib.pyplot as plt
import plots.colors as colors

class Algorithm:
	def __init__(self) -> None:
		pass
	def plot(self, prices, timestamps):
		plt.plot(timestamps, prices, color=colors.primary())
