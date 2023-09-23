from dotenv import load_dotenv
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from views import bot_net_worth, internal_checker, plot

load_dotenv()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

app.add_url_rule('/plot/<algorithm>', view_func=plot.plot)
app.add_url_rule('/internal_checker', view_func=internal_checker.internal_checker)
app.add_url_rule('/profit/<bot_id>',  view_func=bot_net_worth.bot_net_worth)

app.run()