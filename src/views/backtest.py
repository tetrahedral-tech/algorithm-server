import matplotlib as mpl
from backtest_module import backtest, plot
from ipaddress import ip_address
from utils import get_algorithms
from flask import request
from price import get_prices, get_using_coin, get_using_interval

mpl.use('Agg')

def backtest_view(algorithm_name: str):
	if not ip_address(request.remote_addr).is_private:
		return 'Forbidden', 403

	interval = get_using_interval()
	visualize = request.args.get('plot', type=bool, default=False)

	try:
		prices, timestamps, _ = get_prices(interval, get_using_coin())
	except Exception as error:
		return str(error), 400

	if algorithm_name not in [*get_algorithms()]:
		return 'Unsupported Algorithm', 404

	if visualize:
		return plot(backtest(algorithm_name, prices, timestamps, plot=visualize))

	return backtest(algorithm_name, prices, timestamps)
