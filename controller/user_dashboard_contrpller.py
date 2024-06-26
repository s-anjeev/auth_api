from app import app
from model.user_dashboard_model import user_dashboard_model

@app.route('user/dashboard', methods=["GET"])
def dashboard():
    sign_up_obj = user_dashboard_model()
    response = sign_up_obj.user_dashboard()
    
    return response