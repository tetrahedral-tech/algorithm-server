import matplotlib as mpl
from backtest_module import backtest, plot
from ipaddress import ip_address
from utils import get_algorithms
from flask import request
from price import get_prices, get_default_interval, is_supported_interval

mpl.use('Agg')

def backtest_view(algorithm_name: str):
	if not ip_address(request.remote_addr).is_private:
		return 'Forbidden', 403

	interval = int(request.args.get('interval') or get_default_interval())
	plot_bool = bool(request.args.get('plot') or False)

	if algorithm_name not in [*get_algorithms()]:
		return 'Unsupported Algorithm', 404

	if interval and is_supported_interval(interval):
		prices, timestamps, _ = get_prices(interval=interval)
	elif not interval:
		prices, timestamps, _ = get_prices()
	else:
		return 'Unsupported Interval', 400

	if plot_bool:
		return plot(backtest(algorithm_name, prices, timestamps, plot=plot_bool))

	return backtest(algorithm_name, prices, timestamps)
