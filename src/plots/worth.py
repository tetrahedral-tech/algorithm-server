import matplotlib.pyplot as plt
import plots.colors as colors
import numpy as np
from datetime import datetime as dt

def plot(values, timestamps):
	values = np.array(values)
	timestamps = [dt.fromtimestamp(timestamp) for timestamp in timestamps]
	plt.plot(timestamps, values, color=colors.sell())

	return plt
