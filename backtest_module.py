from utils import algorithm_output
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from plots import colors
import io

def backtest(algorithm, prices, balance = 200, strength_to_usd = 190, plot=False): #TODO @fou3fou3 fix prices list with algos IndexError , ValueError
	transactions = []
	start_balance = balance
	shares = 0

	for price in enumerate(prices):
		try:
			singal, strength = algorithm_output(algorithm, prices[0:price[0]], backtest=True)
			usd_amount = strength * strength_to_usd
			shares_amount = usd_amount / price[1]

			if singal in ['buy', 'sell']:
				if singal == 'buy':
					if balance >= usd_amount:
						balance -= usd_amount
						shares += shares_amount
					else:
						shares += balance / price[1]
						balance = 0

				elif singal == 'sell':
					if shares >= shares_amount:
						balance += usd_amount
						shares -= shares_amount
					else:
						balance += shares * price[1]
						shares = 0

				transactions.append({
							'price': price[1],
							'signal': singal,
							'strength': strength,
							'current_balance': balance,
							'current_shares': shares
							})		

		except (IndexError, ValueError):
			pass

	return {
			'transactions': np.array(transactions) if plot else transactions,
			'algorithm': algorithm,  
			'balance': balance, 
			'start_balance': start_balance,
			'final_total': balance + shares * price[1],
			'strength_to_usd': strength_to_usd, 
			'shares': shares,
			'profit': (balance + shares * price[1]) - start_balance,
			'profit_percentage %': ((balance + shares * price[1]) - start_balance) / start_balance 
		}	

def plot(back_test_data):
	gs = GridSpec(3, 1, figure=plt.gcf())
	#@TODO add timestamps @celestials

	indicies = np.arange(back_test_data['transactions'].shape[0])
	balances = [ transaction['current_balance'] for transaction in back_test_data['transactions'] ]
	shares = [ transaction['current_shares'] for transaction in back_test_data['transactions'] ]
	signals = [ transaction['signal'] for transaction in back_test_data['transactions'] ]

	plt.subplot(gs[0, :])
	plt.plot(indicies, balances, color=colors.primary())

	buy_signals = np.where(np.array(signals) == 'buy')[0]
	plt.scatter(buy_signals, [balances[i] for i in buy_signals], color=colors.lower())

	sell_signals = np.where(np.array(signals) == 'sell')[0]
	plt.scatter(sell_signals, [balances[i] for i in sell_signals], color=colors.upper())

	plt.text(indicies[-1], balances[-1] - 2, str(back_test_data['final_total']))
	
	plt.subplot(gs[-1, :])
	plt.plot(indicies, shares, color=colors.primary())
	
	svg_buffer = io.StringIO()
	plt.savefig(svg_buffer, format='svg', transparent=True)
	plot_data = svg_buffer.getvalue()
	plt.close()  # Solved plots overwriting each other
	svg_buffer.close()

	return plot_data