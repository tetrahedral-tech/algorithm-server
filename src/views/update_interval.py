from flask import request
from ipaddress import ip_address
from utils import authorize_server
from price import set_default_interval

def update_interval():
	if not ip_address(request.remote_addr).is_private:
		return 'Forbidden', 403

	if 'interval' not in request.json:
		return 'Bad Request', 400

	try:
		authorize_server(request.headers.get('Authorization'))
	except:
		return 'Unauthorized', 401

	try:
		new_interval = set_default_interval(request.json.interval)
	except Exception as error:
		return str(error), 400

	return str(new_interval)
