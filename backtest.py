import numpy as np
import matplotlib.pyplot as plt
from utils import algorithm_output, svg_plot
from matplotlib.gridspec import GridSpec
from plots import colors

def backtest(algorithm,
             prices,
						 timestamps,
             start_balance=1000,
             strength_to_usd=100,
						 window_size=36):

	transactions = []
	balance = start_balance
	shares = 0

	for window in np.lib.stride_tricks.sliding_window_view(np.column_stack(prices, timestamps), window_size):
		prices_windowed, timestamps_windowed = window

		singal, strength = algorithm_output(algorithm, prices_windowed)
		usd_amount = strength * strength_to_usd
		shares_amount = usd_amount / prices

		if singal in ['buy', 'sell']:
			if singal == 'buy':
				if balance >= usd_amount:
					balance -= usd_amount
					shares += shares_amount
				else:
					shares += balance / prices_windowed[-1]
					balance = 0

			elif singal == 'sell':
				if shares >= shares_amount:
					balance += usd_amount
					shares -= shares_amount
				else:
					balance += shares * prices_windowed[-1]
					shares = 0

			transactions.append({
			  'price': prices_windowed[-1],
			  'signal': singal,
			  'strength': strength,
			  'current_balance': balance,
			  'current_shares': shares,
				'timestamp': timestamps_windowed[-1]
			})

	total = balance + (shares * prices[-1])

	return {
	  'transactions': transactions,
	  'start_balance': start_balance,
	  'net_worth': total,
	  'profit': total - start_balance,
	  'profit_percentage': (total - start_balance) / start_balance
	}

def plot(data):
	gs = GridSpec(3, 1, figure=plt.gcf())

	timestamps = [transaction['timestamp'] for transaction in data['transactions']]
	balances = [transaction['current_balance'] for transaction in data['transactions']]
	shares = [transaction['current_shares'] for transaction in data['transactions']]
	signals = [transaction['signal'] for transaction in data['transactions']]

	plt.subplot(gs[0, :])
	plt.plot(timestamps, balances, color=colors.primary())

	buy_signals = np.where(np.array(signals) == 'buy')[0]
	plt.scatter(buy_signals, [balances[i] for i in buy_signals], color=colors.lower())

	sell_signals = np.where(np.array(signals) == 'sell')[0]
	plt.scatter(sell_signals, [balances[i] for i in sell_signals], color=colors.upper())

	plt.text(timestamps[-1], balances[-1] - 2, str(data['final_total']))

	plt.subplot(gs[-1, :])
	plt.plot(timestamps, shares, color=colors.primary())

	return svg_plot()
