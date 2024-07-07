# import database connection
from utils.db import db_conn
# import input validation code
import mysql.connector
from utils.input_validation import input_validation

from flask import jsonify

class DeleteAccount:
    def __init__(self):
        self.validate_user_input = input_validation()

        db_connection = db_conn()

        self.con = db_connection.conn
        self.cur = db_connection.cur
    
    def delete_account(self,data,user_id):
        try:
            self.user_id_auth = user_id
            self.username = data["username"]
            self.user_id = data["user_id"]
            self.role = data["role"]

            # validating username
            username = self.validate_user_input.username_validation(self.username)
            if username != self.username:
                return jsonify({"error": "Invalid username."}), 400

            vali_user_role = self.validate_user_input.role_validation(self.role)
            if vali_user_role != True:
                return jsonify({"error":"An error occurred while deleting account. Please try again later."}), 400
            
            valid_user_id = self.validate_user_input.user_id_validation(self.user_id)
            if valid_user_id != True:
                return jsonify({"error":"user id cannot be empty"}), 400

            if int(self.user_id) == int(self.user_id_auth):
                return self.delete_account_record(self.user_id_auth)
            else:
                return jsonify({"error": "Unauthorized action"}), 403

        except KeyError as kerr:
            missing_field = kerr.args[0]
            print(f"error : missing key {missing_field}")
            return jsonify({"error": f"Missing field: {missing_field}"}), 400
        except Exception as e:
            print(f"error : {e}")
            return jsonify({"error": "An error occurred while deleting account. Please try again later."}), 500
        

    def delete_account_record(self, user_id):
        delete_session_query = "DELETE FROM session WHERE user_id = %s"
        delete_personal_details_query = "DELETE FROM users_personal_details WHERE user_id = %s"
        delete_user_query = "DELETE FROM users WHERE user_id = %s"
        params = (user_id,)

        try:
            # Delete related records first
            self.cur.execute(delete_session_query, params)
            
            # Delete related records in 'users_personal_details' table
            self.cur.execute(delete_personal_details_query, params)

            # Now delete the user record
            self.cur.execute(delete_user_query, params)
            
            # Commit the transaction after both deletions
            self.con.commit()

        except mysql.connector.Error as err:
            print(f"error : {err}")
            return jsonify({"error": "An error occurred while deleting the account. Please try again later."}), 500
        except Exception as e:
            print(f"error : {e}")
            return jsonify({"error": "An error occurred while deleting the account. Please try again later."}), 500
        finally:
            # Close cursor and connection in finally block to ensure they are always closed
            if self.cur:
                self.cur.close()
            if self.con:
                self.con.close()

        return jsonify({"message": "Account successfully deleted"}), 200
