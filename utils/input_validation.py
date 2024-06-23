import re
from flask import jsonify

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
        

