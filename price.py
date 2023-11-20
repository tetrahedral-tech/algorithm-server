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
def get_prices(pair='ETH-USD', interval=21600):
	ohlc = get(f'https://api.exchange.coinbase.com/products/{pair}/candles?granularity={interval}').json()
	ticker = get(f'https://api.exchange.coinbase.com/products/{pair}/ticker').json()

	current = float(ticker['price'])
	prices = [point[4] for point in ohlc]

	return np.flip([current, *prices])

def get_cached_prices(interval=21600):
	np.array(redis.lrange(f'prices:{interval}', 0, -1))

def get_periods(period_size, period_type, interval):
	if period_type == 'months':
		period_multiplier = 30 * 24 * 60 * 60
	elif period_type == 'weeks':
		period_multiplier = 7 * 24 * 60 * 60
	elif period_type == 'days':
		period_multiplier = 24 * 60 * 60
	elif period_type == 'hours':
		period_multiplier = 60 * 60
	elif period_type == 'minutes':
		period_multiplier = 60
	elif period_type == 'seconds':
		period_multiplier = 1
	period_seconds = period_size * period_multiplier

	return period_seconds / interval

# Price Caching
cachedIntervals = [60, 300, 3600, 21600]

def cache_prices():
	for interval in cachedIntervals:
		print(f'Caching prices for {interval}')
		prices = get_prices(interval=interval)
		redis.lpush(f'prices:{interval}', *prices)

schedule.every(1).minutes.do(cache_prices)

def job_loop():
	while True:
		schedule.run_pending()
		time.sleep(1)

thread = Thread(target=job_loop, daemon=True)
thread.start()
