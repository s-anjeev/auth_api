from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route('/')
def index():
    return jsonify(message="Welcome to the Index Page")

@app.route('/home')
def home():
    return jsonify(message="Welcome to the Home Page")

if __name__ == '__main__':
    app.run(debug=True)


# import user_controller as user_controller
# import product_controller as product controller

# from controller import user_controller,product_controller

from controller import *
# import user_controller

