import jwt, json, os
from redis import Redis
from price import get_prices
from ipaddress import ip_address
from flask import request
from importlib import import_module
from utils import get_algorithms

redis = Redis(host='localhost', port=6379)

def algorithm_output(algorithm, prices):
	module = import_module(f'algorithms.{algorithm}')
	signal = module.signal(module.algorithm(prices))

	# @TODO strength
	return algorithm, (signal, 0.5)

def internal_checker():
	if not ip_address(request.remote_addr).is_private:
		return 'Forbidden', 403

	jwt_encoded = request.headers.get('Authorization')
	if not jwt_encoded:
		return 'Bad Request', 400

	try:
		jwt_decoded = jwt.decode(jwt_encoded, os.environ['JWT_SECRET'], algorithms=['HS256'])
	except Exception as e:
		print(e)
		return 'Unauthorized', 401

	if jwt_decoded['event'] != 'auth':
		return 'Unauthorized', 401

	config = json.load(open('config.json', 'r'))
	prices = get_prices(config['pair'], interval=1440)
	# Convert list of algorithms into {name: signal}
	algorithms = get_algorithms()

	base = dict(map(lambda x: algorithm_output(*x), zip(algorithms, [prices] * len(algorithms))))

	signals = {k: v[0] for (k, v) in base.items()}
	strengths = {k: v[1] for (k, v) in base.items()}

	redis.delete('signals', 'strengths')
	redis.hset('signals', mapping=signals)
	redis.hset('strengths', mapping=strengths)

	return algorithms
