from app import app
from model.user_dashboard_model import user_dashboard_model,AdminGetAllUsers
from utils.aouth_model import token_auth, admin_token_auth

auth = token_auth()

@app.route('/user/dashboard', methods=["GET"])
@auth.token_auth()
def dashboard(user_id):
    sign_up_obj = user_dashboard_model()
    response = sign_up_obj.user_dashboard(user_id)
    
    return response

admin_auth = admin_token_auth()
@app.route('/admin/get-all-users/limit/<limit>/page/<page>', methods = ["GET"])
@auth.token_auth()
def get_all_users(limit,page,admin_id):
    get_all_users_object = AdminGetAllUsers()
    response = get_all_users_object.admin_get_all_users(limit,page,admin_id)

    return response