from flask import jsonify,make_response
from config.config import jwt_secret

import mysql.connector
import jwt
# import database connection
from utils.db import db_conn
# import input validation code
from utils.input_validation import input_validation

class logout_model:
    def __init__(self):
        # Instantiate the input_validation class
        self.validate_user_input = input_validation()
        # Instantiate the db_conn class
        db_connection = db_conn()

        # Access the connection and cursor
        self.conn = db_connection.conn
        self.cur = db_connection.cur

    def user_logout(self, data):
        try:
            self.token = data["token"]
            self.user_id = data["id"]

            try:
                self.id = int(self.user_id)
            except ValueError as ve:
                print(f"Exception: {ve}")
                return jsonify({"error":"Logout failed. Please try again."}), 400
            
            user_session =  self.is_user_session_exist()
            if user_session != False:
                user_id_from_db = user_session[0]["user_id"]
                user_token_from_db = user_session[0]["token"]
            else:
                return jsonify({"error":"Logout failed. Please try again."}), 400
            if user_token_from_db == self.token:
                decoded_token = self.is_valid_session()
            if decoded_token:
                user_id_from_decoded_token = decoded_token["user_id"]
            if user_id_from_decoded_token == user_id_from_db:
                user_log_out = self.delete_user_session(user_id_from_decoded_token)
                return user_log_out

        except KeyError as ke:
            missing_field = ke.args[0]
            return jsonify({"error": f"Missing field: {missing_field}"}), 400
        except Exception as e:
            print(f"Exception: {e}")
            return jsonify({"error": "An error occurred while logging out. Please try again later."}), 500
        

    def is_user_session_exist(self):
        query = "SELECT user_id,token FROM session WHERE user_id=%s"
        params = (self.id,)
        try:
            self.cur.execute(query,params)
            result = self.cur.fetchall()
            if result:
                return result
            else:
                return False
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return jsonify({"error": "An error occurred while logging out. Please try again later."}), 500
    
    def is_valid_session(self):
        # create a jwt token
        secret = jwt_secret["secret"]
        try:
            decoded_token = jwt.decode(self.token,secret,algorithms="HS256")
            return decoded_token
        except jwt.ExpiredSignatureError:
            return make_response({"message":"You have successfully logged out."},401)
    
    def delete_user_session(self, user_id):
        query = "DELETE FROM session WHERE user_id = %s"
        params = (user_id,)
        try:
            self.cur.execute(query, params)
            self.conn.commit()  # Commit the transaction
            return make_response({"message": "You have successfully logged out."}, 200)  # 200 OK for successful logout
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return jsonify({"error": "An error occurred while logging out. Please try again later."}), 500
        finally:
            self.cur.close()  # Ensure the cursor is closed
            self.conn.close()  # Ensure the connection is closed
