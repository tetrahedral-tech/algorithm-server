import io
import matplotlib.pyplot as plt
from price import get_prices
from importlib import import_module

def plot(algorithm):
	prices = get_prices('ETH/USD', interval=1440)

	if algorithm not in ['boillinger_bands', 'macd', 'rsi']:
		return 'Invalid Algorithm', 404
	import_module(f'plots.{algorithm}').plot(prices)

	# Save plot into buffer instead of the FS
	svg_buffer = io.StringIO()
	plt.savefig(svg_buffer, format='svg')
	svg_plot = svg_buffer.getvalue()
	svg_buffer.close()

	return svg_plot