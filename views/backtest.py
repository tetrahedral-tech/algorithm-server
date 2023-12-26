import matplotlib as mpl
from backtest_module import backtest, plot
from utils import get_algorithms
from flask import request
from price import get_prices, get_default_interval, is_cached_interval, get_cached_prices, is_supported_interval

mpl.use('Agg')

def backtest_view(algorithm):
	default_interval = get_default_interval()
	interval = int(request.args.get('interval') or default_interval)
	plot_bool = bool(request.args.get('plot') or False)

	if interval and is_cached_interval(interval):
		prices, _, _ = get_cached_prices(interval=interval)
	elif interval and is_supported_interval(interval):
		prices, _, _ = get_prices(interval=interval)
	elif not interval:
		prices, _, _ = get_cached_prices()
	else:
		return 'Unsupported Interval', 400

	if algorithm not in ['price', *get_algorithms()]:
		return 'Unsupported Algorithm', 404

	if plot_bool:
		return plot(backtest(algorithm, prices, plot=plot_bool))

	return backtest(algorithm, prices)
