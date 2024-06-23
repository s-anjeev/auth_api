from app import app
from flask import jsonify, request
from model.sign_up_model import sign_up_model

@app.route('/sign-up', methods=["POST"])
def sign_up():
    try: 
        # Attempt to parse the JSON data
        data = request.get_json()
        if data is None:
            raise ValueError("No JSON data provided")
    except ValueError as ve:
        return jsonify({"error": "Invalid JSON data", "message": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Bad request", "message": str(e)}), 400
    
    sign_up_obj = sign_up_model()
    response = sign_up_obj.user_sign_up(data)
    
    return response