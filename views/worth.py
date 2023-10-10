import jwt, os, io, utils
import matplotlib.pyplot as plt
import numpy as np
from flask import Response, request
from bson.objectid import ObjectId
from plots.worth import plot
import plots.colors as colors

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

	timestamps, values = np.transpose([[worth['timestamp'] / 1000, worth['value']] for worth in bot['worth']])

	plot(timestamps, values)

	ax = plt.gca()
	ax.tick_params(color=colors.outline(), labelcolor=colors.outline())
	for spine in ax.spines.values():
		spine.set_edgecolor(colors.outline())

	buffer = io.BytesIO()
	plt.savefig(buffer, format='svg', transparent=True)
	value = buffer.getvalue()
	buffer.close()

	return Response(value, mimetype='image/svg+xml')
