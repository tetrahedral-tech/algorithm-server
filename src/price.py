import os
import numpy as np
from redis import from_url
from dotenv import load_dotenv
from flask import has_request_context, request

load_dotenv()
redis = from_url(os.environ['REDIS_URI'])

point_count = 720
default_interval = 240
price_collector_interval = 5
supported_intervals = [5, 15, 30, 60, 240, 1440, 10080]

default_coin = 'WETH'
supported_coins = ['WETH']

def is_supported_interval(interval: int) -> bool:
	global supported_intervals
	return interval in supported_intervals

def is_supported_coin(coin: str) -> bool:
	global supported_coins
	return coin in supported_coins

def get_using_interval() -> int:
	if has_request_context():
		interval = request.args.get('interval', type=int)
		if is_supported_interval(interval):
			return interval
	return default_interval

def get_using_coin() -> str:
	if has_request_context():
		coin = request.args.get('coin')
		if is_supported_coin(coin):
			return coin
	return default_coin

def get_prices(interval, pair):
	if not interval or not pair:
		raise Exception('No Interval/Pair')

	if not is_supported_interval(interval):
		raise Exception(f'Unsupported Interval: {interval}')

	if not is_supported_coin(pair):
		raise Exception(f'Unsupported Pair: {pair}')

	slicing_ratio = int(interval / price_collector_interval)

	prices = redis.lrange(f'{pair}:prices', 0, -1)[::slicing_ratio]
	timestamps = redis.lrange(f'{pair}:timestamps', 0, -1)[::slicing_ratio]

	return np.array(prices).astype(float), np.array(timestamps).astype(int)
