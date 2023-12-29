import jwt, os, io, numpy as np
import matplotlib.pyplot as plt
from pymongo.server_api import ServerApi
from datetime import datetime
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
	module = import_module(f'algorithms.{algorithm}').Algorithm()
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

def interpolate_timestamps(timestamps, interval):
	timestamps = np.array(timestamps, dtype='float64')  # Convert to float
	interval_seconds = interval * 60  # Convert minutes to seconds

	# Calculate the number of intervals needed
	num_intervals = int((timestamps[-1] - timestamps[0]) / interval_seconds) + 1

	# Generate new timestamps using np.arange
	new_timestamps = np.arange(timestamps[0], timestamps[0] + num_intervals * interval_seconds, interval_seconds)

	return new_timestamps
