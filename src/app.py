from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from views import plot, signals, worth, backtest

load_dotenv()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
CORS(app)

app.add_url_rule('/plot/<algorithm_name>', view_func=plot.plot)
app.add_url_rule('/backtest/<algorithm_name>', view_func=backtest.backtest_view)
app.add_url_rule('/worth/<bot_id>', view_func=worth.worth)
app.add_url_rule('/signals', view_func=signals.signals)

if __name__ == '__main__':
	app.run(debug=True)
