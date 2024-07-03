from app import app
from flask import jsonify,request
from model.edit_model import edit_user
from utils.aouth_model import token_auth
from datetime import datetime


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


@app.route('/user/profile/edit/avatar', methods=["PATCH"])
@auth.token_auth()
def edit_avatar(user_id):

    try: 
        # Attempt to parse the JSON data
        try:
            file = request.files['avatar']
            # creating  a unique file name using current time stamp
            unique_file_name = str(datetime.now().timestamp()).replace(".","")
            # getting extention of file 
            file_name_split = file.filename.split(".")
            file_extension = file_name_split[-1]
            # creating a unique url
            unique_file_address = f"{unique_file_name}.{file_extension}"
            # uploading file into uploads directory
            file.save(f"uploads/{unique_file_address}")
        except FileNotFoundError as err:
            return jsonify({"error": "File not foound", "message": str(e)}), 400 
    except Exception as e:
        return jsonify({"error": "Bad request", "message": str(e)}), 400
    

    edit_profile = edit_user()
    return edit_profile.edit_user_avatar(unique_file_address,user_id)