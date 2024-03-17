import os
import numpy as np
from redis import from_url
from dotenv import load_dotenv
from flask import has_request_context, request
from requests import get

load_dotenv()
redis = from_url(os.environ['REDIS_URI'])
price_collector_uri = os.environ['PRICE_COLLECTOR_URI']

point_count = 720
default_interval = 240
price_collector_interval = 5
supported_intervals = [5, 15, 30, 60, 240, 1440]

default_pair = 'USDC-WETH'
supported_pairs = ['USDC-WETH']

def is_supported_interval(interval: int) -> bool:
	global supported_intervals
	return interval in supported_intervals

def is_supported_pair(pair: str) -> bool:
	global supported_pairs
	return pair in supported_pairs

def get_using_interval() -> int:
	if has_request_context():
		interval = request.args.get('interval', type=int)
		if is_supported_interval(interval):
			return interval
	return default_interval

def get_using_pair() -> str:
	if has_request_context():
		pair = request.args.get('pair')
		if is_supported_pair(pair):
			return pair
	return default_pair

def get_prices(interval: int, pair: str, at: int = None):
	if not interval or not pair:
		raise Exception('No Interval/Pair')

	if not is_supported_interval(interval):
		raise Exception(f'Unsupported Interval: {interval}')

	if not is_supported_pair(pair):
		raise Exception(f'Unsupported Pair: {pair}')

	if type(at) != 'int' and at:
		raise Exception(f'Unsupported at timestamp')

	price_api_response = get(f'{price_collector_uri}/prices/{pair}?interval={interval}{f"&at={at}" if at else ""}')
	data = price_api_response.json()

	prices, timestamps = zip(*(item.values() for item in data))

	return np.array(prices).astype(float), np.array(timestamps).astype(int)
