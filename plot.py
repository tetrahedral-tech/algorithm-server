import numpy as np
import matplotlib.pyplot as plt
from price import get_prices
from plots.bollinger_bands import plot as boillinger_bands
from plots.rsi import plot as rsi

prices = get_prices()

# RSI
plt.subplot(221)
rsi(prices)

# Boillinger Bands
plt.subplot(222)
boillinger_bands(prices)

# Prices
plt.subplot(223)
plt.plot(np.arange(0, prices.shape[0]), prices)

plt.show()
