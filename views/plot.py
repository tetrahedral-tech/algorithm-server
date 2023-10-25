import io
import matplotlib.pyplot as plt
from price import get_prices
from importlib import import_module
import plots.colors as colors
import matplotlib

matplotlib.use('Agg')

def plot(algorithm):
	prices = get_prices('ETH/USD', interval=1440)

	if algorithm not in ['bollinger_bands', 'rsi', 'price']:
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
