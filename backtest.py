from algorithms.algorithm_output import algorithm_output

def backtest(algorithm, prices, balance = 200, strength_to_usd = 100): #TODO @fou3fou3 fix prices list with algos IndexError , ValueError
	outputs = []
	start_balance = balance
	shares = 0

	for price in enumerate(prices):
		try:
			singal, strength = algorithm_output(algorithm, prices[0:price[0]], backtest=True)
			usd_amount = strength * strength_to_usd
			shares_amount = usd_amount / price[1]
			if singal == 'buy' and balance >= usd_amount:
				outputs.append((price[1], (singal, strength)))
				balance -= usd_amount
				shares += shares_amount
			elif singal == 'sell' and shares >= shares_amount:
				outputs.append((price[1], (singal, strength)))
				balance += usd_amount
				shares -= shares_amount
		except (IndexError, ValueError):
			pass

	return {
			'outputs': outputs, 
			'algorithm': algorithm,  
			'balance': balance, 
			'start_balance': start_balance,
			'total_balance': balance + shares * price[1],
			'strength_to_usd': strength_to_usd, 
			'shares': shares,
			'profit': (balance + shares * price[1]) - start_balance
		}	