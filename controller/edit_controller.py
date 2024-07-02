from app import app
from flask import jsonify,request
from model.edit_model import edit_user
from utils.aouth_model import token_auth

auth = token_auth()


@app.route('/user/profile/edit', methods=["PATCH"])
@auth.token_auth()
def edit_user_profile(user_id):

    try: 
        # Attempt to parse the JSON data
        data = request.get_json()
        if data is None:
            raise ValueError("No JSON data provided")
    except ValueError as ve:
        return jsonify({"error": "Invalid JSON data", "message": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Bad request", "message": str(e)}), 400

    edit_profile = edit_user()
    return edit_profile.edit_user(data,user_id)