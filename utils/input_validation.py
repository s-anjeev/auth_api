import re
from flask import jsonify
from datetime import datetime
class input_validation():
    def __init__(self):
        pass
    # function for validating username
    def username_validation(self, username):
        username = str(username)
        
        if not username:
            return jsonify({"error": "Username must be 5-12 characters long and contain only alphanumeric characters."}), 400
        
        if len(username) < 5:
            return jsonify({"error": "Username must be 5-12 characters long and contain only alphanumeric characters."}), 400
        
        if len(username) > 12:
            return jsonify({"error": "Username must be 5-12 characters long and contain only alphanumeric characters."}), 400
        
        pattern = re.compile("^[a-zA-Z0-9]+$")
        if pattern.match(username):
            return username
        else:
            return jsonify({"error": "Username must be 5-12 characters long and contain only alphanumeric characters."}), 400

    # function for validating email
    def email_validation(self, email):        
        if not email:
            return jsonify({"error": "Invalid email address."}), 400
        
        # Regular expression for validating an email
        pattern = re.compile(
        r'^(?P<local_part>[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+)@(?P<domain>(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})$'
        )
        is_valid_email =  bool(pattern.match(email))
        if is_valid_email == True:
            return email
        else:
            return jsonify({"error": "Invalid email address."}), 400
    
    # check password strength
    def is_strong_password(self,password):
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[0-9]", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    # function for validating password
    def password_validation(self, password):
        password = str(password)
        
        if not password:
            return jsonify({"error": "Password must be 8-36 characters long and include at least one lowercase letter, one uppercase letter, one number, and one special character."}), 400
        
        if len(password) < 8:
            return jsonify({"error": "Password must be 8-36 characters long and include at least one lowercase letter, one uppercase letter, one number, and one special character."}), 400
        
        if len(password) > 36:
            return jsonify({"error": "Password must be 8-36 characters long and include at least one lowercase letter, one uppercase letter, one number, and one special character."}), 400
        
        strong_pass = self.is_strong_password(password)
        if strong_pass == True:
            return password
        else:
            return jsonify({"error": "Password must be 8-36 characters long and include at least one lowercase letter, one uppercase letter, one number, and one special character."}), 400
        

    # Function to validate first name and last name
    def first_last_name_validation(self, name):
        name = str(name).strip()
        
        if not name:
            return jsonify({"error": "Name must be provided and cannot be empty."}), 400
        
        if len(name) < 3 or len(name) > 20:
            return jsonify({"error": "Name must be between 3-20 characters long."}), 400
        
        if not re.match("^[a-zA-Z\s]+$", name):
            return jsonify({"error": "Name must contain only alphabetic characters and spaces."}), 400

        # If all validations pass
        return True
    
    # validate country code
    def country_validation(self, country_code):
        # Predefined list of valid country codes
        valid_country_codes = ["IND", "USA", "PAK", "CAN", "AUS", "GBR", "FRA", "DEU", "JPN", "CHN"]

        country_code = str(country_code).strip().upper()
        
        if not country_code:
            return jsonify({"error": "Country code must be provided and cannot be empty."}), 400
        
        if country_code not in valid_country_codes:
            return jsonify({"error": "Invalid country code. Please provide a valid country code."}), 400
        
        # If validation passes
        return True

    # Function to validate Indian phone number
    def phone_number_validation(self, phone_number):
        phone_number = str(phone_number).strip()
        
        # Regular expression to match a valid Indian phone number
        pattern = re.compile(r"^[6-9]\d{9}$")
        
        if not phone_number:
            return jsonify({"error": "Phone number must be provided and cannot be empty."}), 400
        
        if not pattern.match(phone_number):
            return jsonify({"error": "Invalid phone number. Phone number must be 10 digits long and start with a digit between 6 and 9."}), 400

        # If validation passes
        return True
    
    # Function to validate date of birth
    def date_of_birth_validation(self, date_of_birth):
        try:
            # Convert the input to a datetime object
            dob = datetime.strptime(date_of_birth, "%Y-%m-%d")
            
            # Check if the date of birth is in the future
            if dob > datetime.today():
                return jsonify({"error": "Date of birth cannot be a future date."}), 400
            
            # If validation passes
            return True
        except ValueError:
            # If the input is not a valid date
            return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD format."}), 400
        

     # Function to validate gender
    def gender_validation(self, gender):
        gender = str(gender).strip().lower()
        
        valid_genders = ["male", "female", "others"]

        if gender not in valid_genders:
            return jsonify({"error": "Invalid gender. Gender must be one of 'male', 'female', or 'others'."}), 400

        # If validation passes
        return True
    
    # Function to validate avatar endpoint
    def avatar_endpoint_validation(self, avatar_url):
        avatar_url = str(avatar_url).strip()

        valid_extensions = ["jpg", "jpeg", "png", "gif", "bmp"]

        # Check if avatar_url starts with '/' and has a valid extension
        if not avatar_url.startswith("/") or not any(avatar_url.lower().endswith(ext) for ext in valid_extensions):
            return jsonify({
                "error": f"Invalid avatar endpoint. Must start with '/' and have one of the following extensions: {', '.join(valid_extensions)}"
            }), 400

        # If validation passes
        return True
    
    # user and admin role validator 
    def role_validation(self,role):
        role = str(role).strip()
        roles = ["user","admin"]
        if role not in roles:
            return jsonify({"error":"An error occurred while deleting account. Please try again later."}), 400
        else:
            return True
        
    # validate user_id 
    def user_id_validation(self,user_id):
        if user_id:
            try:
                user_id = int(user_id)
                return True
            except Exception as e:
                return jsonify({"error":"An error occurred while deleting account. Please try again later."}), 400
        else:
            return jsonify({"error":"user id cannot be empty"}), 400