import schedule, os, time
import numpy as np
from requests import get
from redis import from_url
from dotenv import load_dotenv
from threading import Thread

load_dotenv()
redis = from_url(os.environ['REDIS_URI'])

# {60 300 900  3600   21600  86400}
#  1m 5m  15m  1h     6h     1d
#  5h 25h 3d3h 12d12h 2mo15d 10mo

default_interval = 21600
cached_intervals = [60, 300, 3600, 21600]
supported_intervals = [60, 300, 900, 3600, 21600, 86400]

def set_default_interval(interval):
	global default_interval
	if interval not in supported_intervals:
		raise Exception('Unsupported Interval')

	default_interval = interval
	return default_interval

def get_default_interval():
	return default_interval

def get_prices(pair='ETH-USD', interval=default_interval):
	ohlc = get(f'https://api.exchange.coinbase.com/products/{pair}/candles?granularity={interval}').json()
	ticker = get(f'https://api.exchange.coinbase.com/products/{pair}/ticker').json()

	current = float(ticker['price'])
	prices = [point[4] for point in ohlc]

	return np.flip([current, *prices])

def get_cached_prices(interval=21600):
	return np.array([float(point) for point in redis.lrange(f'prices:{interval}', 0, -1)])

def get_periods(period_size, period_type, interval=default_interval):
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

	return period_seconds / interval

# Price Caching
def cache_prices():
	for interval in cached_intervals:
		print(f'Caching prices for {interval}')
		prices = get_prices(interval=interval)
		redis.delete(f'prices:{interval}')
		redis.lpush(f'prices:{interval}', *prices)

schedule.every(1).minutes.do(cache_prices)
schedule.run_all()

def job_loop():
	while True:
		schedule.run_pending()
		time.sleep(1)

thread = Thread(target=job_loop, daemon=True)
thread.start()
