import io, price
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import plots.colors as colors
from mpld3 import fig_to_html
from flask import request
from importlib import import_module
from utils import get_algorithms

mpl.use('Agg')

figure_size = mpl.rcParams['figure.figsize']
figure_size[0] = figure_size[0] * 1.5

def plot(algorithm):
	default_interval = price.get_default_interval()
	interval = int(request.args.get('interval') or default_interval)
	interactive = bool(request.args.get('interactive') or False)

	if interval and price.is_cached_interval(interval):
		prices, timestamps, _ = price.get_cached_prices(interval=interval)
	elif interval and price.is_supported_interval(interval):
		prices, timestamps, _ = price.get_prices(interval=interval)
	elif not interval:
		prices, timestamps, _ = price.get_cached_prices()
	else:
		return 'Unsupported Interval', 400

	if algorithm not in ['price', *get_algorithms()]:
		return 'Unsupported Algorithm', 404

	# Even out timestamps so plotting algos works
	timestamps = timestamps.astype('datetime64[s]')
	interval_timedelta = np.timedelta64(default_interval, 'm')
	timestamps = np.arange(timestamps[-1] - interval_timedelta * timestamps.shape[0], timestamps[-1], interval_timedelta)

	figure = plt.figure()

	try:
		import_module(f'algorithms.{algorithm}').plot(prices, timestamps)
	except Exception as error:
		return str(error), 400

	axes = figure.get_axes()

	for axis in axes:
		axis.tick_params(color=colors.outline(), labelcolor=colors.outline())
		for spine in axis.spines.values():
			spine.set_edgecolor(colors.outline())

		if interval >= 10080:
			xfmt = md.DateFormatter('%Y')
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

	if interactive:
		# @TODO change d3 and mpld3 urls to local ones
		plot_data = fig_to_html(figure)
	else:
		# Save plot into buffer instead of the FS
		svg_buffer = io.StringIO()
		plt.savefig(svg_buffer, format='svg', transparent=True)
		plot_data = svg_buffer.getvalue()
		plt.close()  # Solved plots overwriting each other
		svg_buffer.close()

	return plot_data
