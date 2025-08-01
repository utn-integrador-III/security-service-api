from functools import wraps
import requests
from flask import request
from decouple import config
import random
import string


def auth_required(action=None, permission='', with_args=False):
    def decorator(f):
        @wraps(f)
        def catcher(*args, **kwargs):
            # Make endpoint in the Auth Service to validate an Auth Token
            # The endpoint will return details such as User's Account ID
            try:
                token = request.headers["Authorization"]
            except:
                return {'message': "Authorization token is required"}, 401
            try:
                #Send Permission to verify if the user has authorization
                body = {'permission': permission}
                response = requests.post(config('AUTH_API_URL') + config('AUTH_API_PORT') + '/auth/verify_auth', json=body, headers={'Authorization': f'JWT {token}'}, timeout=20)
                
            except Exception as ex:
                return {'message': "Error in authentication occurred" + str(ex)}, 500
            # If status code is 200, user is valid
            if response.status_code == 200:
                try:
                    user = response.json()["user"]["username"]
                    if with_args:
                        kwargs['current_user'] = response.json()["user"]
                except:
                    user = None
                #log_action(action, user)
                return f(*args, **kwargs)
            else:
                return response.json(), 401
        return catcher
    return decorator
def generate_verification_code(length=4):
    return ''.join(random.choices(string.digits, k=length))




