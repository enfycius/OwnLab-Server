import jwt
from flask import request, jsonify, current_app, Response
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        if access_token is not None:
            payload = check_access_token(access_token)
            if payload is None:
                return Response(status=401)
        else:
            return Response(status=401)
        return decorated_function
    
    return decorated_function

def check_access_token(access_token):
    try:
        payload = jwt.decode(access_token, "secret", algorithms=["HS256"])
        # if payload['exp'] < datetime.utcnow():
        #     payload = None
    except jwt.InvalidTokenError:
        payload = None
    return payload