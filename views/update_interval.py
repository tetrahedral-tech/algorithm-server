import jwt, os
from flask import request
from ipaddress import ip_address
from price import set_default_interval

def update_interval():
	if not ip_address(request.remote_addr).is_private:
		return 'Forbidden', 403

	jwt_encoded = request.headers.get('Authorization')
	if not jwt_encoded:
		return 'Bad Request', 400

	if 'interval' not in request.json:
		return 'Bad Request', 400

	try:
		jwt_decoded = jwt.decode(jwt_encoded, os.environ['JWT_SECRET'], algorithms=['HS256'])
	except:
		return 'Unauthorized', 401

	if jwt_decoded['event'] != 'auth':
		return 'Unauthorized', 401

	try:
		new_interval = set_default_interval(request.json.interval)
	except Exception as error:
		return str(error), 400

	return new_interval
