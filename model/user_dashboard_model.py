from flask import jsonify, make_response
import mysql.connector
import logging
# import database connection
from utils.db import db_conn

class user_dashboard_model:
    def __init__(self):
        # Instantiate the db_conn class
        db_connection = db_conn()

        # Access the connection and cursor
        self.conn = db_connection.conn
        self.cur = db_connection.cur

    def user_dashboard(self, id):
        self.idd = id
        user_data = self.get_user_data(self.idd)

        if isinstance(user_data, dict) and "error" in user_data:
            return jsonify(user_data), 400
        
        # Extract user details with default values if keys are missing or None
        first_name = user_data[0].get("first_name", "")
        last_name = user_data[0].get("last_name", "")
        country = user_data[0].get("country", "")
        phone_number = user_data[0].get("phone_number", "")
        date_of_birth = user_data[0].get("date_of_birth", "")
        age = user_data[0].get("age", "")
        gender = user_data[0].get("gender", "")
        avatar_url = user_data[0].get("avatar_url", "")

        
        response = {
            "user": {
                "Account": {
                    "user_id": user_data[0]["user_id"],
                    "username": user_data[0]["username"],
                    "role": user_data[0]["role"],
                    "email": user_data[0]["email"]
                },
                "Personal": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "country": country,
                    "phone_number": phone_number,
                    "date_of_birth": date_of_birth,
                    "age": age,
                    "gender": gender,
                    "avatar_url": avatar_url
                }
            }
        }

        return jsonify(response)

    def get_user_data(self, user_id):
        query = "SELECT * FROM userdetailsview WHERE user_id = %s"
        params = (user_id,)
        try:
            self.cur.execute(query, params)
            user_details = self.cur.fetchall()
            if user_details:
                return user_details
            else:
                query = "SELECT * FROM users WHERE user_id = %s"
                params = (user_id,)
                try:
                    self.cur.execute(query, params)
                    user_details = self.cur.fetchall()
                    if user_details:
                        return user_details
                    else:
                        return {"error": "Failed to fetch user account details"}
                except mysql.connector.Error as err:
                    print(f"error: {err}")
                    return {"error": "Failed to fetch user account details"}
        except mysql.connector.Error as err:
            print(f"error: {err}")
            return {"error": "Failed to fetch user account details"}
        


class AdminGetAllUsers:
    def __init__(self):
        db_connection = db_conn()
        self.con = db_connection.conn
        self.cur = db_connection.cur
    
    def admin_get_all_users(self, limit, page, admin_id):
        try:
            # Input validation for limit and page
            if not self.is_valid_limit_page(limit) or not self.is_valid_limit_page(page):
                return jsonify({"error": "Invalid limit or page number"}), 400
            
            self.limit = int(limit)
            self.page = int(page)
            self.admin_id = admin_id

            if self.is_from_admin():
                # Fetch user records from the database
                user_record = self.fetch_user_record()
                return user_record
            else:
                return jsonify({"error": "Unauthorized request"}), 401

        except KeyError as ke:
            missing_field = ke.args[0]
            return jsonify({"error": f"Missing field: {missing_field}"}), 400
        except Exception as e:
            logging.error(f"Exception: {e}")
            return jsonify({"error": "An error occurred while fetching user accounts. Please try again later."}), 500

    def is_valid_limit_page(self, limit_page):
        try:
            limit_page = int(limit_page)
            if limit_page < 1 or limit_page > 10:
                return False
            return True
        except ValueError:
            return False
    
    def is_from_admin(self):
        query = "SELECT * FROM admins WHERE admin_id = %s"
        params = (self.admin_id,)
        try:
            self.cur.execute(query, params)
            is_admin = self.cur.fetchone()
            return is_admin is not None
        except mysql.connector.Error as err:
            logging.error(f"Database error: {err}")
            return False

    def fetch_user_record(self):
        start = (self.page * self.limit) - self.limit
        query = "SELECT * FROM userdetailsview LIMIT %s, %s"
        params = (start, self.limit)
        try:
            self.cur.execute(query, params)
            result = self.cur.fetchall()
            if result:
                res = make_response(jsonify({"users": result}), 200)
                res.headers['Access-Control-Allow-Origin'] = "*"
                return res
            else:
                return make_response(jsonify({"message": "No data found"}), 204)
        except mysql.connector.Error as err:
            logging.error(f"Database error: {err}")
            return jsonify({"error": "Failed to fetch user records"}), 500
