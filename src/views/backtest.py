import matplotlib as mpl
from backtest_module import backtest, plot
from utils import get_algorithms
from flask import request
from price import get_prices, get_default_interval, is_cached_interval, get_cached_prices, is_supported_interval

mpl.use('Agg')

def backtest_view(algorithm_name):
	interval = int(request.args.get('interval') or get_default_interval())
	plot_bool = bool(request.args.get('plot') or False)

	if algorithm_name not in [*get_algorithms()]:
		return 'Unsupported Algorithm', 404

	if interval and is_cached_interval(interval):
		prices, timestamps, _ = get_cached_prices(interval=interval)
	elif interval and is_supported_interval(interval):
		prices, timestamps, _ = get_prices(interval=interval)
	elif not interval:
		prices, timestamps, _ = get_cached_prices()
	else:
		return 'Unsupported Interval', 400

	if plot_bool:
		return plot(backtest(algorithm_name, prices, timestamps, plot=plot_bool))

	return backtest(algorithm_name, prices, timestamps)