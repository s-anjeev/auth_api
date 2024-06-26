from flask import jsonify,make_response
from config.config import jwt_secret

import mysql.connector
import jwt
# import database connection
from utils.db import db_conn
# import input validation code
from utils.input_validation import input_validation

class user_dashboard_model:
    def __init__(self):
        # Instantiate the input_validation class
        self.validate_user_input = input_validation()
        # Instantiate the db_conn class
        db_connection = db_conn()

        # Access the connection and cursor
        self.conn = db_connection.conn
        self.cur = db_connection.cur

    def user_dashboard(self):
        pass