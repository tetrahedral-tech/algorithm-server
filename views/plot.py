from price import get_prices, get_default_interval, get_cached_prices, is_cached_interval, is_supported_interval
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from importlib import import_module
from utils import get_algorithms, svg_plot
from plots.styling import style_plots
from mpld3 import fig_to_html
from flask import request

mpl.use('Agg')

figure_size = mpl.rcParams['figure.figsize']
figure_size[0] = figure_size[0] * 1.5

def plot(algorithm_name):
	interval = int(request.args.get('interval') or get_default_interval())
	interactive = bool(request.args.get('interactive') or False)

	if algorithm_name not in ['price', *get_algorithms()]:
		return 'Unsupported Algorithm', 404

	if interval and is_cached_interval(interval):
		prices, timestamps, _ = get_cached_prices(interval=interval)
	elif interval and is_supported_interval(interval):
		prices, timestamps, _ = get_prices(interval=interval)
	elif not interval:
		prices, timestamps, _ = get_cached_prices()
	else:
		return 'Unsupported Interval', 400

	# Even out timestamps so plotting algos works
	timestamps = timestamps.astype('datetime64[s]')
	interval_timedelta = np.timedelta64(interval, 'm')
	timestamps = np.arange(timestamps[-1] - interval_timedelta * timestamps.shape[0], timestamps[-1], interval_timedelta)

	figure = plt.figure()

	try:
		algorithm = import_module(f'algorithms.{algorithm_name}').Algorithm()
		algorithm.plot(prices=prices, timestamps=timestamps)
	except Exception as error:
		return str(error), 400

	style_plots(interval)

	# @TODO change d3 and mpld3 urls to local ones
	return fig_to_html(figure) if interactive else svg_plot()
