import os
from flask import request
from redis import from_url
from price import get_prices, is_supported_interval
from ipaddress import ip_address
from utils import get_algorithms, algorithm_output

redis = from_url(os.environ['REDIS_URI'])
last_checked_point = 0

def signals():
	global last_checked_point
	if not ip_address(request.remote_addr).is_private:
		return 'Forbidden', 403

	interval = request.args.get('interval', type=int)
	coin = request.args.get('coin', type=str)

	if 'interval' not in request.json or 'coin' not in request.json:
		return 'Bad Request', 400

	try:
		prices, _, _ = get_prices(interval=interval, pair=coin)
	except:
		return 'Unsupported Interval', 400

	# Convert list of algorithms into {name: signal}
	algorithms = get_algorithms()

	base = dict(map(lambda x: algorithm_output(*x), zip(algorithms, [prices] * len(algorithms))))

	signals = {k: v[0] for (k, v) in base.items()}
	# strengths = {k: v[1] for (k, v) in base.items()}

	return signals
