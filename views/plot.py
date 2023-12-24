from price import get_prices, get_default_interval, get_cached_prices, is_cached_interval, is_supported_interval
import matplotlib.pyplot as plt
import plots.colors as colors
import matplotlib.dates as md
import matplotlib as mpl
import numpy as np
import io
from algorithms.algorithm_output import algorithm_output
from importlib import import_module
from utils import get_algorithms
from mpld3 import fig_to_html
from flask import request

mpl.use('Agg')

figure_size = mpl.rcParams['figure.figsize']
figure_size[0] = figure_size[0] * 1.5

def plot(algorithm):
	default_interval = get_default_interval()
	interval = int(request.args.get('interval') or default_interval)
	interactive = bool(request.args.get('interactive') or False)
	backtest = bool(request.args.get('backtest') or False)

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
	elif backtest:
		outputs = []
		balance = 200 # love money $$
		strength_to_usd = 25
		start_balance = balance
		shares = 0
		for price in enumerate(prices):
			try:
				singal, strength = algorithm_output(algorithm, prices[0:price[0]])
				usd_amount = strength * strength_to_usd
				shares_amount = usd_amount / price[1]
				if singal == 'buy' and balance >= usd_amount:
					outputs.append((price[1], (singal, strength)))
					balance -= usd_amount
					shares += shares_amount
				elif singal == 'sell' and shares >= shares_amount:
					outputs.append((price[1], (singal, strength)))
					balance += usd_amount
					shares -= shares_amount
			except (IndexError, ValueError):
				pass
		backtest_data = {
			'outputs': outputs, 
			'algorithm': algorithm,  
			'balance': balance, 
			'start_balance': start_balance,
			'total_balance': balance + shares * price[1],
			'strength_to_usd': strength_to_usd, 
			'shares': shares,
			'profit': (balance + shares * price[1]) - start_balance
		}	
		return backtest_data	
	else:
		# Save plot into buffer instead of the FS
		svg_buffer = io.StringIO()
		plt.savefig(svg_buffer, format='svg', transparent=True)
		plot_data = svg_buffer.getvalue()
		plt.close()  # Solved plots overwriting each other
		svg_buffer.close()

	return plot_data
