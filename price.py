import os
import numpy as np
from requests import get
from redis import from_url
from dotenv import load_dotenv
from flask import has_request_context, request

load_dotenv()
redis = from_url(os.environ['REDIS_URI'])

#  1   5     15    30   60  240  1440 10080 21600
#  12h 2d12h 1w12h 2w1d 1mo 4mo  2y   14y   30y

point_count = 720
default_interval = 240
cached_intervals = [30, 60, 240, 1440]
supported_intervals = [1, 5, 15, 30, 60, 240, 1440, 10080]

def is_supported_interval(interval):
	global supported_intervals
	return interval in supported_intervals

def is_cached_interval(interval):
	global cached_intervals
	return interval in cached_intervals

def set_default_interval(interval):
	global default_interval
	if not is_supported_interval(interval):
		raise Exception('Unsupported Interval')

	default_interval = interval
	return default_interval

def get_default_interval():
	if has_request_context():
		interval = request.args.get('interval')
		if interval and is_supported_interval(int(interval)):
			return int(interval)
	return default_interval

def get_prices(pair='ETH/USD', interval='default'):
	if interval == 'default':
		interval = get_default_interval()

	ohlc = get(f'https://api.kraken.com/0/public/OHLC?pair={pair}&interval={interval}').json()

	if 'result' not in ohlc:
		raise Exception(ohlc['error'][0])

	results = list(ohlc['result'].values())[0]

	# [:-1] to trim off the uncomplete datapoint
	timestamps = [point[0] for point in results][:-1]
	prices = [float(point[4]) for point in results][:-1]
	last_complete_point = ohlc['result']['last']

	return np.array(prices).astype(float), np.array(timestamps).astype(float), last_complete_point

def get_cached_prices(interval='default'):
	if interval == 'default':
		interval = get_default_interval()

	if not is_cached_interval(interval):
		raise Exception('Uncached Interval')

	prices = redis.lrange(f'prices:{interval}', 0, -1)
	timestamps = redis.lrange(f'timestamps:{interval}', 0, -1)
	last_complete_point = redis.get(f'last_complete_point:{interval}')

	if len(prices) < 1:
		return np.zeros(point_count), np.zeros(point_count)

	return np.array(prices).astype(float), np.array(timestamps).astype(float), float(last_complete_point)

# Price Caching
def update_cached_prices():
	for interval in cached_intervals:
		print(f'Caching prices for {interval}')
		prices, timestamps, last_complete_point = get_prices(interval=interval)

		redis.delete(f'prices:{interval}')
		redis.delete(f'timestamps:{interval}')
		redis.set(f'last_complete_point:{interval}', last_complete_point)
		redis.rpush(f'prices:{interval}', *prices.tolist())
		redis.rpush(f'timestamps:{interval}', *timestamps.tolist())
