from app import app
from flask import jsonify


@app.route('/login')
def login():
    return jsonify(message="Welcome to the login Page")