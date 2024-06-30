from flask import jsonify, make_response
from config.config import jwt_secret
import mysql.connector
import jwt
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
