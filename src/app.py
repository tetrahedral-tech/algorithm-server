import schedule, time
from threading import Thread
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from price import update_cached_prices
from views import internal_checker, plot, worth, interval, update_interval, backtest

load_dotenv()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
CORS(app)

app.add_url_rule('/plot/<algorithm_name>', view_func=plot.plot)
app.add_url_rule('/backtest/<algorithm_name>', view_func=backtest.backtest_view)
app.add_url_rule('/worth/<bot_id>', view_func=worth.worth)
app.add_url_rule('/interval', view_func=interval.interval)
app.add_url_rule('/internal_checker', view_func=internal_checker.internal_checker)
app.add_url_rule('/update_interval', view_func=update_interval.update_interval, methods=['POST'])

def job_loop():
	while True:
		schedule.run_pending()
		time.sleep(1)

def start_price_cache():
	schedule.every(2.5).minutes.do(update_cached_prices)
	schedule.run_all()

	thread = Thread(target=job_loop, daemon=True)
	thread.start()

if __name__ == '__main__':
	start_price_cache()
	app.run()
