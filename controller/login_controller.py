from app import app
from flask import jsonify,request
# from model.login_model import
from model.login_model import login_model
@app.route('/login', methods=["POST"])
def login(): 
    try: 
        # Attempt to parse the JSON data
        data = request.get_json()
        if data is None:
            raise ValueError("No JSON data provided")
    except ValueError as ve:
        return jsonify({"error": "Invalid JSON data", "message": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Bad request", "message": str(e)}), 400

    login_obj = login_model()
    response = login_obj.user_login(data)

    return response