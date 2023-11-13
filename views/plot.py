import json, io
import matplotlib
import matplotlib.pyplot as plt
import plots.colors as colors
from utils import get_algorithms
from price import get_prices
from importlib import import_module
from utils import get_algorithms

matplotlib.use('Agg')

def plot(algorithm):
	config = json.load(open('config.json', 'r'))
	prices = get_prices(address=config['address'] if 'address' in config else None)

	if algorithm not in get_algorithms():
		return 'Invalid Algorithm', 404
	import_module(f'plots.{algorithm}').plot(prices)

	ax = plt.gca()
	ax.tick_params(color=colors.outline(), labelcolor=colors.outline())
	for spine in ax.spines.values():
		spine.set_edgecolor(colors.outline())

	# Save plot into buffer instead of the FS
	svg_buffer = io.StringIO()
	plt.savefig(svg_buffer, format='svg', transparent=True)
	svg_plot = svg_buffer.getvalue()
	plt.close()  # Solved plots overwriting each other
	svg_buffer.close()

	return svg_plot
