import jwt, os
from redis import from_url
from price import get_prices
from ipaddress import ip_address
from flask import request
from importlib import import_module
from utils import get_algorithms

redis = from_url(os.environ['REDIS_URI'])

def algorithm_output(algorithm, prices):
	module = import_module(f'algorithms.{algorithm}')
	signal, strength = module.signal(prices, module.algorithm(prices))

	return algorithm, (signal, strength)

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

	prices = get_prices()

	# Convert list of algorithms into {name: signal}
	algorithms = get_algorithms()

	base = dict(map(lambda x: algorithm_output(*x), zip(algorithms, [prices] * len(algorithms))))

	signals = {k: v[0] for (k, v) in base.items()}
	strengths = {k: v[1] for (k, v) in base.items()}

	redis.delete('signals', 'strengths')
	redis.hset('signals', mapping=signals)
	redis.hset('strengths', mapping=strengths)

	return algorithms
