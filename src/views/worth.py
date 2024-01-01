import utils
import numpy as np
import matplotlib as mpl
from plots.styling import style_plots
from flask import request
from bson.objectid import ObjectId
from plots.worth import plot

mpl.use('Agg')
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

	style_plots()
	return utils.svg_plot()