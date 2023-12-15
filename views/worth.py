import io, utils
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as md
import plots.colors as colors
from flask import Response, request
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

	axes = plt.gcf().get_axes()

	for axis in axes:
		axis.tick_params(color=colors.outline(), labelcolor=colors.outline())
		for spine in axis.spines.values():
			spine.set_edgecolor(colors.outline())

		xfmt = md.DateFormatter('%y/%m')
		axis.xaxis.set_major_formatter(formatter=xfmt)

	plt.tight_layout()

	buffer = io.BytesIO()
	plt.savefig(buffer, format='svg', transparent=True)
	value = buffer.getvalue()
	plt.close()
	buffer.close()

	return Response(value, mimetype='image/svg+xml')
