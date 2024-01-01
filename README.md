# Auto Trading Project (Algorithm-Server)

## Overview

This is an algorithmic trading project that uses technical analysis indicators such as Bollinger Bands, RSI, MACD, and custom algorithms. The project fetches cryptocurrency price data from the Kraken API at different intervals: 1, 5, 15, 30, 60, 240, 1440, 10080 minutes.

The trading logic is implemented in a Flask web application that serves as an API to provide data to the main server responsible for executing trades. The web application has several views:

- **Backtest**: Allows backtesting of algorithms with different intervals.
  - Sub-view: **Backtest Plot**: Plots backtest profits, buy/sell signals, and additional information.

- **Plot**: Plots algorithms and displays their buy/sell timings over 720 prices of different intervals.

- **Internal Checker**: Enables communication between the main server and the algorithm server to fetch algorithm data.

## Features

- **Technical Indicators**: Implements Bollinger Bands, RSI, MACD, and custom algorithms for trading decisions.
  
- **Kraken API Integration**: Fetches cryptocurrency prices at various intervals.

- **Flask Web Application**: Provides a user interface with flask-views for backtesting, plotting.

- **Backtesting**: Evaluate algorithms with historical data to assess performance.

- **Plotting**: Visual representation of algorithmic performance and buy/sell timings.

- **Internal Checker**: Facilitates communication between the main server and algorithm server.

- **Redis**: The application uses redis for optomization and reaching cached prices rapidly.

## Getting Started

### Prerequisites

- Python 3.10 and higher
- Install required Python packages: `conda activate auto-trading && conda env update -n auto-trading --file environment.yml` on linux/unix
- Install redis using: `sudo apt-get update && sudo apt-get install redis `

### Configuration

1. Configure jwt, mongo-db-uri, redis-uri parameters in `.env` you can use `example.env` for help.

### Usage

1. Run the Flask web application: `python app.py`
2. Access the views in a web browser:
   - Backtest: `http://localhost:5000/backtest/{algorithm_name}?interval=integer&plot=boolean`
   - Plot: `http://localhost:5000/plot/{algorithm_name}?interval=integer`
   - Internal Checker: `http://localhost:5000/internal-checker?interval=integer`

## Screenshots

screenshot*

## Contributing

This is a closed source application only members of organization can contribute.

## License

All rights reserved. This project is closed source and proprietary. No part of this project may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the project owner.

For licensing inquiries, please contact us.

