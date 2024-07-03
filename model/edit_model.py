from flask import jsonify, make_response
from datetime import datetime
import mysql.connector
from utils.db import db_conn
from utils.input_validation import input_validation

class edit_user:
    def __init__(self):
        self.validate_user_input = input_validation()
        db_connection = db_conn()
        self.conn = db_connection.conn
        self.cur = db_connection.cur

    def edit_user(self, data, user_id):
        try:
            user_id = user_id  # This should come from your authentication function

            first_name = data.get("first_name")
            last_name = data.get("last_name")
            country = data.get("country")
            phone_number = data.get("phone_number")
            date_of_birth = data.get("date_of_birth")
            gender = data.get("gender")

            # Validate first and last names
            first_name_valid = self.validate_user_input.first_last_name_validation(first_name)
            if first_name_valid is not True:
                return first_name_valid
            
            last_name_valid = self.validate_user_input.first_last_name_validation(last_name)
            if last_name_valid is not True:
                return last_name_valid

            # Validate country code
            country_valid = self.validate_user_input.country_validation(country)
            if country_valid is not True:
                return country_valid

            # Validate phone number
            phone_number_valid = self.validate_user_input.phone_number_validation(phone_number)
            if phone_number_valid is not True:
                return phone_number_valid

            # Validate date of birth
            if date_of_birth:
                date_of_birth_valid = self.validate_user_input.date_of_birth_validation(date_of_birth)
                if date_of_birth_valid is not True:
                    return date_of_birth_valid
                date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
                age = self.calculate_age(date_of_birth)
            else:
                date_of_birth = None
                age = None

            # Validate gender
            gender_valid = self.validate_user_input.gender_validation(gender)
            if gender_valid is not True:
                return gender_valid

            # Validate avatar endpoint
            # avatar_valid = self.validate_user_input.avatar_endpoint_validation(avatar_url)
            # if avatar_valid is not True:
            #     return avatar_valid


            # Check if user exists in the Users_personal_details table
            query_search = "SELECT * FROM Users_personal_details WHERE user_id = %s"
            param_search = (user_id,)
            self.cur.execute(query_search, param_search)
            record_exist = self.cur.fetchone()  # Use fetchone to get a single record

            # Clear any remaining results to avoid the Unread result found error
            self.cur.fetchall()

            if record_exist:
                # Update user details
                query_update = """
                UPDATE Users_personal_details 
                SET first_name = %s, last_name = %s, country = %s, phone_number = %s, date_of_birth = %s, gender = %s 
                WHERE user_id = %s
                """
                params_update = (first_name, last_name, country, phone_number, date_of_birth, gender, user_id)
                self.cur.execute(query_update, params_update)
                self.conn.commit()
                return make_response(jsonify({"message": "Account details updated successfully."}), 200)
            else:
                # Insert new user details
                query_insert = """
                INSERT INTO Users_personal_details (first_name, last_name, country, phone_number, date_of_birth, age, gender, user_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                params_insert = (first_name, last_name, country, phone_number, date_of_birth, age, gender, user_id)
                self.cur.execute(query_insert, params_insert)
                self.conn.commit()
                return make_response(jsonify({"message": "Account details inserted successfully."}), 200)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return jsonify({"error": "An error occurred while updating account details. Please try again later."}), 500
        except KeyError as ke:
            missing_field = ke.args[0]
            return jsonify({"error": f"Missing field: {missing_field}"}), 400
        except Exception as e:
            print(f"Exception: {e}")
            return jsonify({"error": "An error occurred while updating account details. Please try again later."}), 500
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                self.conn.close()

    def calculate_age(self, date_of_birth):
        today = datetime.today()
        return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))


    # upload user avatar
    def edit_user_avatar(self, unique_file_address, user_id):
        try:
            avatar_url = unique_file_address

            # Validate avatar endpoint
            avatar_valid = self.validate_user_input.avatar_endpoint_validation(avatar_url)
            if not avatar_valid:
                return avatar_valid


            # Check if user exists in the Users_personal_details table
            query_search = "SELECT * FROM Users_personal_details WHERE user_id = %s"
            param_search = (user_id,)
            self.cur.execute(query_search, param_search)
            record_exist = self.cur.fetchone()  # Use fetchone to get a single record

            # Clear any remaining results to avoid the Unread result found error
            self.cur.fetchall()

            if record_exist:
                # Update user details
                query_update = """
                UPDATE Users_personal_details 
                SET avatar_url = %s
                WHERE user_id = %s
                """
                params_update = (avatar_url, user_id)
                self.cur.execute(query_update, params_update)
                self.conn.commit()
                return make_response(jsonify({"message": "Account details updated successfully."}), 200)
            else:
                # Insert new user details
                query_insert = """
                INSERT INTO Users_personal_details (avatar_url, user_id) 
                VALUES (%s, %s)
                """
                params_insert = (avatar_url, user_id)
                self.cur.execute(query_insert, params_insert)
                self.conn.commit()
                return make_response(jsonify({"message": "Account details inserted successfully."}), 200)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return jsonify({"error": "An error occurred while updating account details. Please try again later."}), 500
        except KeyError as ke:
            missing_field = ke.args[0]
            return jsonify({"error": f"Missing field: {missing_field}"}), 400
        except Exception as e:
            print(f"Exception: {e}")
            return jsonify({"error": "An error occurred while updating account details. Please try again later."}), 500
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                self.conn.close()