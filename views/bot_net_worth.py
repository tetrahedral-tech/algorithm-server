import jwt, os, io, utils
from flask import request
import matplotlib.pyplot as plt
from bson.objectid import ObjectId
from plots.bot_net_worth import plot

def get_net_worth(bot_id):
	bots = utils.client['database']['bots']
	bot_worth = bots.find_one({'_id': ObjectId(bot_id)})['worth']
	
	return [worth['value'] for worth in bot_worth]

def bot_net_worth(bot_id):
	jwt_encoded = request.headers.get('Authorization')
	if not jwt_encoded:
		return 'Bad Request', 400

	try:
		jwt_decoded = jwt.decode(jwt_encoded, os.environ['JWT_SECRET'], algorithms=['HS256'])
		if jwt_decoded._id != bot_id:
			raise 'Token Mismatch'
	except Exception:
		return 'Unauthorized', 401

	plot(get_net_worth(bot_id))

	svg_buffer = io.StringIO()
	plt.savefig(svg_buffer, format='svg')
	svg_plot = svg_buffer.getvalue()
	svg_buffer.close()

	return svg_plot
