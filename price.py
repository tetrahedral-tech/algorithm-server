import schedule, os, time
import numpy as np
from math import ceil
from requests import get
from redis import from_url
from dotenv import load_dotenv
from threading import Thread
from flask import has_request_context, request

load_dotenv()
redis = from_url(os.environ['REDIS_URI'])

# {60 300 900  3600   21600  86400}
#  1m 5m  15m  1h     6h     1d
#  5h 25h 3d3h 12d12h 2mo15d 10mo

point_count = 300
default_interval = 21600
cached_intervals = [300, 900, 3600, 21600]
supported_intervals = [60, 300, 900, 3600, 21600, 86400]

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

def get_prices(pair='ETH-USD', interval='default'):
	if interval == 'default':
		interval = get_default_interval()

	ohlc = get(f'https://api.exchange.coinbase.com/products/{pair}/candles?granularity={interval}').json()

	prices = [point[4] for point in ohlc]
	timestamps = [point[0] for point in ohlc]

	return np.flip(prices), np.flip(timestamps)

def get_cached_prices(interval='default'):
	if interval == 'default':
		interval = get_default_interval()

	if not is_cached_interval(interval):
		raise Exception('Uncached Interval')

	prices = redis.lrange(f'prices:{interval}', 0, -1)
	timestamps = redis.lrange(f'timestamps:{interval}', 0, -1)

	if len(prices) < 1:
		return np.zeros(point_count), np.zeros(point_count)

	return np.array(prices).astype(float), np.array(timestamps).astype(float)

def get_periods(period_size, period_type, interval='default'):
	if interval == 'default':
		interval = get_default_interval()

	if 'month' in period_type:
		period_multiplier = 30 * 24 * 60 * 60
	elif 'week' in period_type:
		period_multiplier = 7 * 24 * 60 * 60
	elif 'day' in period_type:
		period_multiplier = 24 * 60 * 60
	elif 'hour' in period_type:
		period_multiplier = 60 * 60
	elif 'minute' in period_type:
		period_multiplier = 60
	elif 'second' in period_type:
		period_multiplier = 1
	period_seconds = period_size * period_multiplier

	return max(ceil(period_seconds / interval), 2)

# Price Caching
def cache_prices():
	for interval in cached_intervals:
		print(f'Caching prices for {interval}')
		prices, timestamps = get_prices(interval=interval)

		redis.delete(f'prices:{interval}')
		redis.lpush(f'prices:{interval}', *prices.tolist())

		redis.delete(f'timestamps:{interval}')
		redis.lpush(f'timestamps:{interval}', *timestamps.tolist())

schedule.every(3).minutes.do(cache_prices)

def job_loop():
	schedule.run_all()
	while True:
		schedule.run_pending()
		time.sleep(1)

thread = Thread(target=job_loop, daemon=True)
thread.start()
