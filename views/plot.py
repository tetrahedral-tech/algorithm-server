import io
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import plots.colors as colors
from flask import request
from importlib import import_module
from price import get_cached_prices, get_prices, is_cached_interval, is_supported_interval, get_default_interval
from utils import get_algorithms

matplotlib.use('Agg')

def plot(algorithm):
	interval = int(request.args.get('interval'))

	if interval and is_cached_interval(interval):
		prices, timestamps = get_cached_prices(interval=interval)
	elif interval and is_supported_interval(interval):
		prices, timestamps = get_prices(interval=interval)
	elif not interval:
		prices, timestamps = get_cached_prices()
	else:
		return 'Unsupported Interval', 400

	if algorithm not in ['price', *get_algorithms()]:
		return 'Unsupported Algorithm', 404

	# Even out timestamps so plotting algos works
	timestamps = timestamps.astype('datetime64[s]')
	interval_timedelta = np.timedelta64(get_default_interval(), 's')
	timestamps = np.arange(timestamps[0], timestamps[0] + interval_timedelta * 300, interval_timedelta)

	import_module(f'plots.{algorithm}').plot(prices, timestamps)

	axes = plt.gcf().get_axes()
	for axis in axes:
		axis.tick_params(color=colors.outline(), labelcolor=colors.outline())
		for spine in axis.spines.values():
			spine.set_edgecolor(colors.outline())
			if interval <= 3600:
				xfmt = md.DateFormatter('%d')
			elif interval <= 21600:
				xfmt = md.DateFormatter('%m/%d')
			else:
				xfmt = md.DateFormatter('%m')
			axis.xaxis.set_major_formatter(xfmt)

	plt.tight_layout()

	# Save plot into buffer instead of the FS
	svg_buffer = io.StringIO()
	plt.savefig(svg_buffer, format='svg', transparent=True)
	svg_plot = svg_buffer.getvalue()
	plt.close()  # Solved plots overwriting each other
	svg_buffer.close()

	return svg_plot
