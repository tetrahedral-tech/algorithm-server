import pandas as pd

def algorithm(prices, window_sizes=[12, 26, 9]):
	prices = pd.DataFrame(prices)

	macd = prices.ewm(span=window_sizes[0], adjust=False).mean() - prices.ewm(span=window_sizes[1], adjust=False).mean()
	signal = macd.ewm(span=window_sizes[2], adjust=False).mean()

	return macd.to_numpy().squeeze(), signal.to_numpy().squeeze()

def signal(data):
	macd, signal = data
	# Done i made it "not stupid XD"
	if macd[-1] > signal[-1]:
		return 'sell'
	elif macd[-1] < signal[-1]:
		return 'buy'
	return 'no_action'
