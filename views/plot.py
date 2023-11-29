import io
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import plots.colors as colors
from flask import request
from importlib import import_module
from price import get_cached_prices, get_prices, is_cached_interval, is_supported_interval, get_default_interval
from utils import get_algorithms

mpl.use('Agg')

figure_size = mpl.rcParams['figure.figsize']
figure_size[0] = figure_size[0] * 1.5

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
	interval_timedelta = np.timedelta64(get_default_interval(), 'm')
	timestamps = np.arange(timestamps[-1] - interval_timedelta * timestamps.shape[0], timestamps[-1], interval_timedelta)

	try:
		import_module(f'plots.{algorithm}').plot(prices, timestamps)
	except Exception as error:
		return str(error), 400

	axes = plt.gcf().get_axes()
	for axis in axes:
		axis.tick_params(color=colors.outline(), labelcolor=colors.outline())
		for spine in axis.spines.values():
			spine.set_edgecolor(colors.outline())
			if interval >= 10080:
				xfmt = md.DateFormatter(fmt='%Y')
			elif interval >= 1440:
				xfmt = md.DateFormatter('%y/%m')
			elif interval >= 240:
				xfmt = md.DateFormatter('%m/%d')
			elif interval >= 15:
				xfmt = md.DateFormatter('%d')
			else:
				xfmt = md.DateFormatter('%H')

			axis.xaxis.set_major_formatter(formatter=xfmt)

	plt.tight_layout()

	# Save plot into buffer instead of the FS
	svg_buffer = io.StringIO()
	plt.savefig(svg_buffer, format='svg', transparent=True)
	svg_plot = svg_buffer.getvalue()
	plt.close()  # Solved plots overwriting each other
	svg_buffer.close()

	return svg_plot
