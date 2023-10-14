import matplotlib.pyplot as plt
import plots.colors as colors
import datetime as dt
import numpy as np

def plot(timestamps, values):
	values = np.array(values)
	# times = [ dt.datetime.fromtimestamp(timestamp) for timestamp in timestamps ]
	times = np.arange(0, values.shape[0]) * 5
	plt.plot(times, values, color=colors.upper())

	return plt
