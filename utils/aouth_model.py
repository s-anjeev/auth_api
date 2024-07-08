from flask import make_response, request
from config.config import jwt_secret
from functools import wraps
import jwt
import re

class token_auth():
    def __init__(self):
        pass

    def token_auth(self):  
        def inner1(func):
            @wraps(func)
            def inner2(*args, **kwargs):
                # Fetch the Authorization header
                auth_token = request.headers.get("authorization")
                token = None
                if auth_token:
                    # Check the format of the Authorization header
                    if re.match(r"^Bearer\s+(\S+)$", auth_token):
                        # Extract the token
                        split_auth_token = auth_token.split(" ")
                        token = split_auth_token[1]
                        try:
                            secret = jwt_secret["secret"]
                            decoded_token = jwt.decode(token, secret, algorithms="HS256")
                            admin_id = decoded_token["admin_id"]
                            # print(decoded_token)
                            # Pass the admin_id to the endpoint function
                            kwargs['admin_id'] = admin_id
                        except jwt.ExpiredSignatureError:
                            return make_response({"error": "token expired"}, 401)
                        except jwt.InvalidTokenError:
                            return make_response({"error": "invalid token"}, 401)
                    else:
                        return make_response({"error": "invalid token format"}, 401)
                else:
                    return make_response({"error": "missing Authorization header"}, 401)
                
                return func(*args, **kwargs)
            return inner2
        return inner1



class admin_token_auth():
    def __init__(self):
        pass

    def token_auth(self):  
        def inner1(func):
            @wraps(func)
            def inner2(*args, **kwargs):
                # Fetch the Authorization header
                auth_token = request.headers.get("authorization")
                token = None
                if auth_token:
                    # Check the format of the Authorization header
                    if re.match(r"^Bearer\s+(\S+)$", auth_token):
                        # Extract the token
                        split_auth_token = auth_token.split(" ")
                        token = split_auth_token[1]
                        try:
                            secret = jwt_secret["secret"]
                            decoded_token = jwt.decode(token, secret, algorithms="HS256")
                            admin_id = decoded_token["admin_id"]
                            # print(decoded_token)
                            # Pass the admin_id to the endpoint function
                            kwargs['admin_id'] = admin_id
                        except jwt.ExpiredSignatureError:
                            return make_response({"error": "token expired"}, 401)
                        except jwt.InvalidTokenError:
                            return make_response({"error": "invalid token"}, 401)
                    else:
                        return make_response({"error": "invalid token format"}, 401)
                else:
                    return make_response({"error": "missing Authorization header"}, 401)
                
                return func(*args, **kwargs)
            return inner2
        return inner1
