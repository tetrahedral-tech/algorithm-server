import os
from flask import request
from redis import from_url
from price import get_prices, get_default_interval, is_supported_interval, get_cached_prices, is_supported_interval, is_cached_interval
from ipaddress import ip_address
from utils import authorize_server, get_algorithms, algorithm_output

redis = from_url(os.environ['REDIS_URI'])
last_checked_point = 0

def internal_checker():
	global last_checked_point
	if not ip_address(request.remote_addr).is_private:
		return 'Forbidden', 403

	try:
		authorize_server(request.headers.get('Authorization'))
	except Exception:
		return 'Unauthorized', 401

	interval = int(request.args.get('interval') or get_default_interval())

	if interval and is_cached_interval(interval):
		prices, _, last_complete_point = get_cached_prices(interval=interval)
	elif interval and is_supported_interval(interval):
		prices, _, last_complete_point = get_prices(interval=interval)
	elif not interval:
		prices, _, last_complete_point = get_cached_prices()
	else:
		return 'Unsupported Interval', 400

	new_datapoint = last_complete_point > last_checked_point
	if new_datapoint:
		last_checked_point = last_complete_point

	# Convert list of algorithms into {name: signal}
	algorithms = get_algorithms()

	if new_datapoint:
		base = dict(map(lambda x: algorithm_output(*x), zip(algorithms, [prices] * len(algorithms))))

		signals = {k: v[0] for (k, v) in base.items()}
		strengths = {k: v[1] for (k, v) in base.items()}

		redis.delete('signals', 'strengths')
		redis.hset('signals', mapping=signals)
		redis.hset('strengths', mapping=strengths)

	return {'algorithms': algorithms, 'new_datapoint': new_datapoint}
