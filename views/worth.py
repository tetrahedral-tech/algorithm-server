import io, utils
import matplotlib.pyplot as plt
import numpy as np
from flask import Response, request
from bson.objectid import ObjectId
from plots.worth import plot
import plots.colors as colors
import matplotlib

matplotlib.use('Agg')
bots = utils.client['database']['bots']

def worth(bot_id):
	try:
		bot = bots.find_one({'_id': ObjectId(bot_id)})
		decoded = utils.authorize(request.headers.get('Authorization'))
		if decoded['_id'] != str(bot['owner']):
			raise 'Token Mismatch'
	except Exception:
		return 'Unauthorized', 401

	if len(bot['worth']) == 0:
		plot([], [])
	else:
		timestamps, values = np.transpose([[worth['timestamp'] / 1000, worth['value']] for worth in bot['worth']])
		plot(values, timestamps)

	ax = plt.gca()
	ax.tick_params(color=colors.outline(), labelcolor=colors.outline())
	for spine in ax.spines.values():
		spine.set_edgecolor(colors.outline())

	buffer = io.BytesIO()
	plt.savefig(buffer, format='svg', transparent=True)
	value = buffer.getvalue()
	plt.close()
	buffer.close()

	return Response(value, mimetype='image/svg+xml')
