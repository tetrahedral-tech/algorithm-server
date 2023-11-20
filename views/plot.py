import io
import matplotlib
import matplotlib.pyplot as plt
import plots.colors as colors
from flask import request
from importlib import import_module
from utils import get_algorithms
from price import get_cached_prices
from utils import get_algorithms

matplotlib.use('Agg')

def plot(algorithm):
	interval = request.args.get('interval')
	if interval:
		prices = get_cached_prices(interval=interval)
	else:
		prices = get_cached_prices()

	if algorithm not in ['price', *get_algorithms()]:
		return 'Invalid Algorithm', 404
	import_module(f'plots.{algorithm}').plot(prices)

	axes = plt.gcf().get_axes()
	for axis in axes:
		axis.tick_params(color=colors.outline(), labelcolor=colors.outline())
		for spine in axis.spines.values():
			spine.set_edgecolor(colors.outline())

	plt.tight_layout()

	# Save plot into buffer instead of the FS
	svg_buffer = io.StringIO()
	plt.savefig(svg_buffer, format='svg', transparent=True)
	svg_plot = svg_buffer.getvalue()
	plt.close()  # Solved plots overwriting each other
	svg_buffer.close()

	return svg_plot
