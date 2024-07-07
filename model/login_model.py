from flask import jsonify,make_response
from datetime import datetime,timedelta
from config.config import jwt_secret,hash_config
import mysql.connector
import hashlib
import jwt
# import database connection
from utils.db import db_conn
# import input validation code
from utils.input_validation import input_validation

class login_model:
    def __init__(self):
        # Instantiate the input_validation class
        self.validate_user_input = input_validation()
        # Instantiate the db_conn class
        db_connection = db_conn()

        # Access the connection and cursor
        self.conn = db_connection.conn
        self.cur = db_connection.cur

    def user_login(self, data):
        try:
            self.email = data["email"]
            self.password = data["password"]

            # validate email address
            email = self.validate_user_input.email_validation(self.email)
            if email != self.email:
                return jsonify({"error":"Login failed. Please check your email and password,"}), 400
            
            # check if user exist or not
            is_user = self.is_user_exist()
            if is_user == False:
                return jsonify({"error":"Login failed. Please check your email and password,"}), 400
            
            # check if supplied password match with the actual password
            correct_password = self.is_right_password(is_user[0]["password_hash"])
            if correct_password == False:
                return jsonify({"error":"Login failed. Please check your email and password,"}), 400
            
            # calculating expire time
            exp_time = datetime.now() + timedelta(minutes=60)
            exp_epoch_time = int(exp_time.timestamp())

            user={
                "user_id":is_user[0]["user_id"],
                "username":is_user[0]["username"],
                "email":is_user[0]["email"],
                "role":is_user[0]["role"],
                "exp": exp_epoch_time  # Using 'exp' for the expiration time claim
            }

            # create a jwt token
            secret = jwt_secret["secret"]
            TOKEN = jwt.encode(user, secret, algorithm="HS256")
            # return token to user
            response ={
                "success":"Login successful.",
                "token":TOKEN

            }
            if self.store_session(is_user[0]["user_id"],TOKEN):
                # login successful
                return make_response({"user": response}, 200)
            else:
                return jsonify({"error": "An error occurred while logging in. Please try again later."}), 500
                
        except KeyError as ke:
            missing_field = ke.args[0]
            return jsonify({"error": f"Missing field: {missing_field}"}), 400
        except Exception as e:
            print(f"Exception: {e}")
            return jsonify({"error": "An error occurred while logging in. Please try again later."}), 500
    
    def is_user_exist(self):
        query = "SELECT * FROM users WHERE email=%s"
        params = (self.email,)
        try:
            self.cur.execute(query,params)
            result = self.cur.fetchall()
            if result:
                return result
            else:
                return False
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return jsonify({"error": "An error occurred while logging in. Please try again later."}), 500
        
    def is_right_password(self,password_hash):
        password = self.password
        # Generate a salt
        salt = hash_config["salt"].encode('utf-8')
        
        # Convert password to bytes
        password_bytes = password.encode('utf-8')
        salted_password = salt + password_bytes
        
        # Hash using SHA-256 (or another suitable hash function)
        hash_func = hashlib.sha256()
        hash_func.update(salted_password)
        hashed_password = hash_func.hexdigest()
        if hashed_password == password_hash:
            return True
        else:
            return False

    def store_session(self, user_id, token):

        query_search = "SELECT * FROM session WHERE user_id = %s"
        param_search = (user_id,)
        try:
            self.cur.execute(query_search, param_search)
            search_result = self.cur.fetchall()
            if search_result:
                query = "UPDATE session SET token = %s WHERE user_id = %s"
                params = (token, user_id)
            else:
                query = "INSERT INTO session (user_id, token) VALUES (%s, %s)"
                params = (user_id, token)
            
            self.cur.execute(query, params)
            self.conn.commit()  # Commit the transaction
            return True  # Return True if the operation is successful

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False  # Return False if there's an error

        finally:
            # Close cursor and connection in finally block to ensure they are always closed
            if self.cur:
                self.cur.close()
            if self.conn:
                self.conn.close()




class LoginModel:
    def __init__(self):
        # Instantiate the input_validation class
        self.validate_user_input = input_validation()
        # Instantiate the db_conn class
        db_connection = db_conn()

        # Access the connection and cursor
        self.conn = db_connection.conn
        self.cur = db_connection.cur

    def admin_login(self, data):
        try:
            email = data["email"]
            password = data["password"]
            # Validate email address
            validated_email = self.validate_user_input.email_validation(email)
            if validated_email != email:
                return jsonify({"error": "Login failed. Please check your email and password."}), 400

            # Check if admin exists
            is_admin = self.is_admin_exist(email)
            if not is_admin:
                return jsonify({"error": "Login failed. Please check your email and password."}), 400

            # Check if supplied password matches the stored password hash
            correct_password = self.is_right_password_admin(password, is_admin[0]["password_hash"])
            if not correct_password:
                return jsonify({"error": "Login failed. Please check your email and password."}), 400
            
            # Calculate expiration time
            exp_time = datetime.now() + timedelta(minutes=60)
            exp_epoch_time = int(exp_time.timestamp())

            user = {
                "admin_id": is_admin[0]["admin_id"],
                "email": is_admin[0]["email"],
                "role": is_admin[0]["role"],
                "exp": exp_epoch_time  # Using 'exp' for the expiration time claim
            }

            # Create a JWT token
            try:
                secret = jwt_secret["secret"]
                TOKEN = jwt.encode(user, secret, algorithm="HS256")
            except Exception as e:
                print(f"JWT Encoding Exception: {e}")
                return jsonify({"error": "An error occurred while logging in. Please try again later."}), 500

            # Store session token
            if self.store_session(is_admin[0]["admin_id"], TOKEN):
                response = {
                    "success": "Login successful.",
                    "token": TOKEN
                }
                return make_response(jsonify({"user": response}), 200)
                
            else:
                return jsonify({"error": "An error occurred while logging in. Please try again later."}), 500

        except KeyError as ke:
            missing_field = ke.args[0]
            return jsonify({"error": f"Missing field: {missing_field}"}), 400
        except Exception as e:
            print(f"Exception: {e}")
            return jsonify({"error": "An error occurred while logging in. Please try again later."}), 500

    def is_admin_exist(self, email):
        query = "SELECT * FROM Admins WHERE email=%s"
        params = (email,)
        try:
            self.cur.execute(query, params)
            result = self.cur.fetchall()
            if result:
                return result
            else:
                return False
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return jsonify({"error": "An error occurred while logging in. Please try again later."}), 500

    def store_session(self, admin_id, token):
        query_search = "SELECT * FROM Admins WHERE admin_id = %s"
        param_search = (admin_id,)
        try:
            self.cur.execute(query_search, param_search)
            search_result = self.cur.fetchall()
            if search_result:
                query = "UPDATE Admins SET session_token = %s WHERE admin_id = %s"
                params = (token, admin_id)
            else:
                query = "INSERT INTO Admins (admin_id, session_token) VALUES (%s, %s)"
                params = (admin_id, token)
            
            self.cur.execute(query, params)
            self.conn.commit()  # Commit the transaction
            return True  # Return True if the operation is successful

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False  # Return False if there's an error

        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                self.conn.close()

    def is_right_password_admin(self, password, password_hash):
        # Generate a salt
        salt = hash_config["salt"].encode('utf-8')
        
        # Convert password to bytes
        password_bytes = password.encode('utf-8')
        salted_password = salt + password_bytes
        
        # Hash using SHA-256 (or another suitable hash function)
        hash_func = hashlib.sha256()
        hash_func.update(salted_password)
        hashed_password = hash_func.hexdigest()
        return hashed_password == password_hash
    