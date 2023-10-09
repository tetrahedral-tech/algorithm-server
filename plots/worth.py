import matplotlib.pyplot as plt
import plots.colors as colors
import datetime as dt
import numpy as np

def plot(timestamps, value):
	value = np.array(value)
	# times = [ dt.datetime.fromtimestamp(timestamp) for timestamp in timestamps ]
	times = np.indicies(0, value.shape[0]) * 5
	plt.plot(times, value, color=colors.upper())

	return plt
