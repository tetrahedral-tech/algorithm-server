import os
import numpy as np
from redis import from_url
from dotenv import load_dotenv
from flask import has_request_context, request

load_dotenv()
redis = from_url(os.environ['REDIS_URI'])

point_count = 720
default_interval = 240
price_api_interval = 5
supported_intervals = [5, 15, 30, 60, 240, 1440, 10080]

def is_supported_interval(interval: int) -> bool:
	global supported_intervals
	return interval in supported_intervals

def set_default_interval(interval: int) -> int:
	global default_interval
	if not is_supported_interval(interval):
		raise Exception('Unsupported Interval')

	default_interval = interval
	return default_interval

# Get the default interval
def get_default_interval() -> int:
	if has_request_context():
		interval = request.args.get('interval')
		if interval and is_supported_interval(int(interval)):
			return int(interval)
	return default_interval

def get_prices(interval='default', pair='WETH'):
	if interval == 'default':
		interval = get_default_interval()

	slicing_ratio = int(interval / price_api_interval)

	prices = redis.lrange(f'{pair}:prices', 0, -1)[::slicing_ratio]
	timestamps = redis.lrange(f'{pair}:timestamps', 0, -1)[::slicing_ratio]
	last_complete_point = prices[-1]
	return np.array(prices).astype(float), np.array(timestamps).astype(int), float(last_complete_point)
