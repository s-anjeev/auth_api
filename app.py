from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

app = Flask(__name__)
CORS(app) 

# Initialize rate limiting
# limiter = Limiter(
#     app,
#     key_func=get_remote_address,
#     default_limits=["200 per day", "50 per hour"]
# )

# Initialize logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return jsonify(message="Welcome to the Index Page")

if __name__ == '__main__':
    app.run(debug=True)


from controller import *
# import user_controller

