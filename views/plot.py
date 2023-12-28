from price import get_prices, get_default_interval, get_cached_prices, is_cached_interval, is_supported_interval
import matplotlib.pyplot as plt
import matplotlib as mpl
from importlib import import_module
from utils import get_algorithms, svg_plot
from plots.styling import style_plots
from mpld3 import fig_to_html
from flask import request

mpl.use('Agg')

figure_size = mpl.rcParams['figure.figsize']
figure_size[0] = figure_size[0] * 1.5

def plot(algorithm):
	default_interval = get_default_interval()
	interval = int(request.args.get('interval') or default_interval)
	interactive = bool(request.args.get('interactive') or False)

	if interval and is_cached_interval(interval):
		prices, timestamps, _ = get_cached_prices(interval=interval)
	elif interval and is_supported_interval(interval):
		prices, timestamps, _ = get_prices(interval=interval)
	elif not interval:
		prices, timestamps, _ = get_cached_prices()
	else:
		return 'Unsupported Interval', 400

	if algorithm not in ['price', *get_algorithms()]:
		return 'Unsupported Algorithm', 404

	figure = plt.figure()

	try:
		import_module(f'algorithms.{algorithm}').plot(prices, timestamps)
	except Exception as error:
		return str(error), 400

	style_plots(interval)

		# @TODO change d3 and mpld3 urls to local ones
	return fig_to_html(figure) if interactive else svg_plot()
