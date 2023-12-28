import jwt, os, io, numpy as np
import matplotlib.pyplot as plt
from pymongo.server_api import ServerApi
from pymongo import MongoClient
from dotenv import load_dotenv
from importlib import import_module

load_dotenv()

client = MongoClient(os.environ['DB_URI'], server_api=ServerApi('1'))
algorithms = client['database']['algorithms']

def get_algorithms():
	return [algorithm['name'] for algorithm in algorithms.find({'owner': {'$not': {'$type': 'object'}}})]

def authorize(encoded):
	if encoded.startswith('Bearer'):
		encoded = encoded[7:]

	return jwt.decode(encoded, os.environ['JWT_SECRET'], algorithms=['HS256'])

def authorize_server(encoded):
	decoded = authorize(encoded)

	if not decoded['server']:
		raise Exception('Client Token')

	return decoded

def algorithm_output(algorithm, prices, backtest=False):
	module = import_module(f'algorithms.{algorithm}')
	signal, strength = module.signal(prices, module.algorithm(prices))
	if backtest:
		return signal, strength

	return algorithm, (signal, strength)

def svg_plot():
	svg_buffer = io.StringIO()
	plt.savefig(svg_buffer, format='svg', transparent=True)
	plot_data = svg_buffer.getvalue()
	plt.close()
	svg_buffer.close()

	return plot_data

def interpolate_timestamps(timestamps, interval, datetime_type='s'):
	timestamps = np.array(timestamps, dtype='datetime64[s]')
	interval_timedelta = np.timedelta64(interval, 'm')
	timestamps = np.arange(timestamps[-1] - interval_timedelta * timestamps.shape[0], timestamps[-1], interval_timedelta)
	return timestamps