from flask import jsonify,make_response,json
import mysql.connector
from flask import request
from functools import wraps
import jwt
import re
from config.config import  db_config

  
class auth_model():
    def __init__(self):
        # connection establishment code
        try:
            self.conn = mysql.connector.connect(host=db_config["host"], user=db_config["username"], password=db_config["password"], database=db_config["database"])
            self.cur = self.conn.cursor(dictionary=True)
            print("connection established successfully")
        except Exception as e:
            print(f"{e}")

    # def token_auth(self, endpoint):
    #     def inner1(func):
    #         def inner2(*args, **kwargs):
    #         # You can add token authentication logic here
    #         # For now, we simply call the original function
    #             return func(*args, **kwargs)
    #         return inner2
    #     return inner1
     
    def token_auth(self, endpoint=""):  
        endpoint = [endpoint]
        def inner1(func):
            @wraps(func)
            def inner2(*args, **kwargs):
                endpoint = request.url_rule.rule
                endpoint = [endpoint]
                # Fetch the Authorization header
                auth_token = request.headers.get("authorization")
                # print(auth_token)
                token = None
                if auth_token:
                    # Check the format of the Authorization header
                    if re.match(r"^Bearer\s+(\S+)$", auth_token):
                        # Extract the token
                        split_auth_token = auth_token.split(" ")
                        token = split_auth_token[1]
                        try:
                            decoded_token = jwt.decode(token,"sanjeev",algorithms="HS256")
                        except jwt.ExpiredSignatureError:
                            return make_response({"error":"token expired"},401)
                        role_id = decoded_token["role_id"]
                        # role_id=str(role_id)
                        # print(role_id)
                        # interact with database
                        query = "SELECT roles FROM accessibility_view WHERE endpoint = %s"
                        self.cur.execute(query,endpoint)
                        result = self.cur.fetchall()
                        if result:
                            roles = json.loads(result[0]["roles"])
                            if role_id in roles:
                                return func(*args, **kwargs)
                            else:
                                return make_response({"error":"forbidden"},403)
                        else:
                            return make_response({"error":"Unknown endpoint"},404)
                    else:
                        return make_response({"error": "invalid token"}, 401)
                else:
                    return make_response({"error": "missing Authorization header"}, 401)
            return inner2
        return inner1
