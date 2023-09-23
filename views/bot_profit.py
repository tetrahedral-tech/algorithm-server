import jwt, os, io
from flask import request
from utils import get_bot_profit
from plots.bot_profit import plot
import matplotlib.pyplot as plt

def bot_profit(bot_id):
  jwt_encoded = request.headers.get('Authorization')
  if not jwt_encoded:
    return 'Bad Request', 400 
 
  try:
    jwt_decoded = jwt.decode(jwt_encoded, os.environ['JWT_SECRET'], algorithms=['HS256'])
  except Exception as e:
    print(e)
    return 'Unauthorized', 401
  
  profits = get_bot_profit(bot_id)
  plot(profits)
  
  svg_buffer = io.StringIO()
  plt.savefig(svg_buffer, format='svg')
  svg_plot = svg_buffer.getvalue()
  svg_buffer.close()

  return svg_plot