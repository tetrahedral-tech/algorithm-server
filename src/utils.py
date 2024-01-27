import jwt, os, io
import matplotlib.pyplot as plt
from pymongo.server_api import ServerApi
from pymongo import MongoClient
from dotenv import load_dotenv
from importlib import import_module

load_dotenv()

client = MongoClient(os.environ['DB_URI'], server_api=ServerApi('1'))
algorithms = client['database']['algorithms']

def get_algorithms() -> list[str]:
	return [algorithm['name'] for algorithm in algorithms.find({'owner': {'$not': {'$type': 'object'}}})]

def authorize(encoded: str) -> str:
	if encoded.startswith('Bearer'):
		encoded = encoded[7:]

	return jwt.decode(encoded, os.environ['JWT_SECRET'], algorithms=['HS256'])

def authorize_server(encoded: str) -> str:
	decoded = authorize(encoded)

	if not decoded['server']:
		raise Exception('Client Token')

	return decoded

def algorithm_output(algorithm_name: str, prices: list[float], backtest=False) -> tuple[str, tuple[str, float]]:
	module = import_module(f'algorithms.{algorithm_name}').Algorithm()
	signal, strength = module.signal(prices, module.algorithm(prices))
	if backtest:
		return signal, strength

	return algorithm_name, (signal, strength)

def svg_plot() -> str:
	svg_buffer = io.StringIO()
	plt.savefig(svg_buffer, format='svg', transparent=True)
	plot_data = svg_buffer.getvalue()
	plt.close()
	svg_buffer.close()

	return plot_data