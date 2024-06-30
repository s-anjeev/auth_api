from app import app
from model.user_dashboard_model import user_dashboard_model
from utils.aouth_model import token_auth

auth = token_auth()

@app.route('/user/dashboard', methods=["GET"])
@auth.token_auth()
def dashboard(user_id):
    sign_up_obj = user_dashboard_model()
    response = sign_up_obj.user_dashboard(user_id)
    
    return response