from app import app
from flask import jsonify,request
# from model.login_model import
from model.logout_model import logout_model,logoutmodel

@app.route('/logout', methods=["GET"])
def logout(): 
    try: 
        # Attempt to parse the JSON data
        data = request.get_json()
        if data is None:
            raise ValueError("No JSON data provided")
    except ValueError as ve:
        return jsonify({"error": "Invalid JSON data", "message": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Bad request", "message": str(e)}), 400

    login_obj = logout_model()
    response = login_obj.user_logout(data)

    return response


@app.route('/admin/logout', methods=["GET"])
def adminlogout(): 
    try: 
        # Attempt to parse the JSON data
        data = request.get_json()
        if data is None:
            raise ValueError("No JSON data provided")
    except ValueError as ve:
        return jsonify({"error": "Invalid JSON data", "message": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Bad request", "message": str(e)}), 400

    login_obj = logoutmodel()
    response = login_obj.admin_logout(data)

    return response