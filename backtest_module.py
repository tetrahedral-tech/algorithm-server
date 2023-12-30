from utils import algorithm_output
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from plots import colors
import io

def backtest(algorithm, prices, timestamps, balance=200, strength_to_usd=190, plot=False):
	transactions = []
	start_balance = balance
	shares = 0

	for index, price in enumerate(prices, 1):
		signal, strength = algorithm_output(algorithm, prices[0:index], backtest=True)
		usd_amount = strength * strength_to_usd
		shares_amount = usd_amount / price

		if signal in ['buy', 'sell']:
			if signal == 'buy':
				if balance >= usd_amount:
					balance -= usd_amount
					shares += shares_amount
				else:
					shares += balance / price
					balance = 0
			elif signal == 'sell':
				if shares >= shares_amount:
					balance += usd_amount
					shares -= shares_amount
				else:
					balance += shares * price
					shares = 0

			transactions.append({
			  'price': price,
			  'signal': signal,
			  'strength': strength,
			  'current_balance': balance,
			  'current_shares': shares,
			  'timestamp': timestamps[index - 1]
			})

	return {
	  'transactions': np.array(transactions) if plot else transactions,
	  'algorithm': algorithm,
	  'balance': balance,
	  'start_balance': start_balance,
	  'final_total': balance + shares * price,
	  'strength_to_usd': strength_to_usd,
	  'shares': shares,
	  'profit': (balance + shares * price) - start_balance,
	  'profit_percentage %': (((balance + shares * price) - start_balance) / start_balance) * 100
	}

def plot(back_test_data):
	gs = GridSpec(3, 1, figure=plt.gcf())

	timestamps = [transaction['timestamp'] for transaction in back_test_data['transactions']]
	balances = [transaction['current_balance'] for transaction in back_test_data['transactions']]
	shares = [transaction['current_shares'] for transaction in back_test_data['transactions']]
	signals = [transaction['signal'] for transaction in back_test_data['transactions']]

	plt.subplot(gs[0, :])
	plt.plot(timestamps, balances, color=colors.primary())

	buy_signals = np.where(np.array(signals) == 'buy')[0]
	plt.scatter(buy_signals, [balances[i] for i in buy_signals], color=colors.lower())

	sell_signals = np.where(np.array(signals) == 'sell')[0]
	plt.scatter(sell_signals, [balances[i] for i in sell_signals], color=colors.upper())

	plt.text(timestamps[-1], balances[-1] - 2, str(back_test_data['final_total']))

	plt.subplot(gs[-1, :])
	plt.plot(timestamps, shares, color=colors.primary())

	svg_buffer = io.StringIO()
	plt.savefig(svg_buffer, format='svg', transparent=True)
	plot_data = svg_buffer.getvalue()
	plt.close()  # Solved plots overwriting each other
	svg_buffer.close()

	return plot_data
