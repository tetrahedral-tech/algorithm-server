import jwt, os
from pymongo.server_api import ServerApi
from pymongo import MongoClient
from dotenv import load_dotenv

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
