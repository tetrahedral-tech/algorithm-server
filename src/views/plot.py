from price import get_prices, get_using_coin, get_using_interval, is_supported_interval
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from importlib import import_module
from utils import get_algorithms, svg_plot, timestamps_range
from plots.styling import style_plots
from mpld3 import fig_to_html
from flask import request

mpl.use('Agg')

figure_size = mpl.rcParams['figure.figsize']
figure_size[0] = figure_size[0] * 1.5

def plot(algorithm_name: str):
	interval = get_using_interval()
	pair = get_using_coin()
	interactive = request.args.get('interactive', type=bool, default=False)

	if algorithm_name not in ['price', *get_algorithms()]:
		return 'Unsupported Algorithm', 404

	from_time = int(request.args.get('from') or False)
	to_time = int(request.args.get('to') or -1)

	try:
		prices, timestamps = get_prices(interval, pair)
		if from_time:
			prices, timestamps = timestamps_range(from_time, to_time, prices, timestamps)
	except Exception as error:
		return str(error)

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
