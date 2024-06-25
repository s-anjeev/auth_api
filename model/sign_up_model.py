from flask import jsonify
import hashlib
from config.config import hash_config
import mysql.connector
# import database connection
from utils.db import db_conn
# import input validation code
from utils.input_validation import input_validation

class sign_up_model:
    def __init__(self):
        # Instantiate the input_validation class
        self.validate_user_input = input_validation()

        # Instantiate the db_conn class
        db_connection = db_conn()

        # Access the connection and cursor
        self.conn = db_connection.conn
        self.cur = db_connection.cur

    def user_sign_up(self, data):
        try:
            self.email = data["email"]
            self.username = data["username"]
            self.password = data["password"]

            # validate email address
            email = self.validate_user_input.email_validation(self.email)
            if email != self.email:
                return jsonify({"error": "Invalid email address."}), 400
            # validating username
            username = self.validate_user_input.username_validation(self.username)
            if username != self.username:
                return jsonify({"error": "Invalid username."}), 400
            # validating password
            password = self.validate_user_input.password_validation(self.password)
            if str(password) != str(self.password):
                return jsonify({"error": "Password must be 8-36 characters long and include at least one lowercase letter, one uppercase letter, one number, and one special character."}), 400
            

            existing_user = self.is_username_exist(self.username)
            if existing_user:
                return jsonify({"error": "Username already in use."}), 400
            
            existing_email = self.is_email_exist(self.email)
            if existing_email:
                return jsonify({"error": "Email already in use."}), 400
            
            # generate hash of password
            password_hash = self.password_hash(self.password)

            query = "INSERT INTO users (email, username, password_hash) VALUES(%s, %s, %s);"
            params = (self.email, self.username, password_hash)
                        
            try:
                self.cur.execute(query, params)
                self.conn.commit()
                # account created successfully
                return jsonify({"message": "User account created successfully"}), 201
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return jsonify({"error": "An error occurred while creating the account. Please try again later."}), 500
            finally:
                self.cur.close()
                self.conn.close()
        
        except KeyError as ke:
            missing_field = ke.args[0]
            return jsonify({"error": f"Missing field: {missing_field}"}), 400
        except Exception as e:
            print(f"Exception: {e}")
            return jsonify({"error": "An error occurred while creating the account. Please try again later."}), 500
    
    def is_username_exist(self, username):
        # Check if a username exists in the users table
        query = "SELECT username FROM users WHERE username = %s"
        params = (username,)
        try:
            self.cur.execute(query, params)
            result = self.cur.fetchone()
            return result is not None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
    
    def is_email_exist(self, email):
        # Check if a email exists in the users table
        query = "SELECT email FROM users WHERE email = %s"
        params = (email,)
        try:
            self.cur.execute(query, params)
            result = self.cur.fetchone()
            return result is not None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        
    def password_hash(self, password):
        # Generate a salt
        salt = hash_config["salt"].encode('utf-8')
        
        # Convert password to bytes
        password_bytes = password.encode('utf-8')
        salted_password = salt + password_bytes
        
        # Hash using SHA-256 (or another suitable hash function)
        hash_func = hashlib.sha256()
        hash_func.update(salted_password)
        hashed_password = hash_func.hexdigest()
        
        # Return hashed password
        return hashed_password
