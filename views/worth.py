import jwt, os, io, utils
from flask import Response, request
import matplotlib.pyplot as plt
from bson.objectid import ObjectId
from plots.worth import plot

bots = utils.client['database']['bots']

def worth(bot_id):
	jwt_encoded = request.headers.get('Authorization')
	if not jwt_encoded:
		return 'Bad Request', 400

	try:
		bot = bots.find_one({'_id': ObjectId(bot_id)})
		jwt_decoded = jwt.decode(jwt_encoded, os.environ['JWT_SECRET'], algorithms=['HS256'])
		if jwt_decoded['_id'] != str(bot['owner']):
			raise 'Token Mismatch'
	except Exception:
		return 'Unauthorized', 401

	plot([worth['value'] for worth in bot['worth']])

	buffer = io.BytesIO()
	plt.savefig(buffer, format='svg')
	value = buffer.getvalue()
	buffer.close()

	return Response(value, mimetype='image/svg+xml')
