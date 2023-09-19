from numpy.lib.stride_tricks import sliding_window_view

def algorithm(prices, window_size=20, standard_deviations=2):
	windowed_prices = sliding_window_view(prices, window_size)

	middle_band = windowed_prices.mean(axis=-1)
	std_dev = windowed_prices.std(axis=-1) * standard_deviations

	upper_band = middle_band + std_dev
	lower_band = middle_band - std_dev

	return upper_band, lower_band, middle_band

def signal(data):
	upper_band, lower_band, middle_band = data
	if middle_band[-1] > upper_band[-1]:
		return 'sell', 1
	if middle_band[-1] < lower_band[-1]:
		return 'buy', 0.5
	return 'no_action', 0
