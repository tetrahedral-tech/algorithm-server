import app

bind = '0.0.0.0:80'
workers = 2
loglevel = 'info'
captureoutput = True

on_starting = lambda server: app.start_price_cache()
