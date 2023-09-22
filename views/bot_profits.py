import jwt, os
from flask import request

def profit(bot_id):
  jwt_encoded = request.headers.get('Authorization')
  if not jwt_encoded:
    return 'Bad Request', 400 
 
  try:
    jwt_decoded = jwt.decode(jwt_encoded, os.environ['JWT_SECRET'], algorithms=['HS256'])
  except Exception as e:
    print(e)
    return 'Unauthorized', 401

  return 'Request Accepted'