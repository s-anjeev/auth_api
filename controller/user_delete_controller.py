from app import app
from flask import request, jsonify
from model.account_delete_model import  DeleteAccount
from utils.aouth_model import token_auth

auth = token_auth()

@app.route("/user/delete-account", methods=["GET"])
@auth.token_auth()
def delete_account(user_id):
    try:
        data = request.get_json()
        if data is None:
            raise ValueError("No JSON data provided")
    except ValueError as ve:
        print(f"Error : {ve}")
        return jsonify({"error": "Invalid JSON data", "message": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Bad request", "message": str(e)}), 400
    
    obj = DeleteAccount()
    response = obj.delete_account(data,user_id)

    return response
