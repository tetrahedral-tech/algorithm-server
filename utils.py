import os
from pymongo.server_api import ServerApi
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.environ['DB_URI'], server_api=ServerApi('1'))
algorithms = client['database']['algorithms']
bots = client['database']['bots']

def get_algorithms():
	return [
		algorithm['name']
		for algorithm
		in algorithms.find({ 'owner': { '$not': { '$type': 'object' } } })
	]
 
def get_bot_profit(bot_id):
    bot_id = ObjectId(bot_id)
    bot = bots.find_one({"_id": bot_id})
    profits = bot['profits']

    return profits

