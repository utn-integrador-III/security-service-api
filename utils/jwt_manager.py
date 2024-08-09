import jwt
from datetime import datetime, timedelta
from decouple import config

def generate_jwt(identity, rolName, email):
    """
    Generate a JSON Web Token (JWT) for the given identity with additional details
    """
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=30),  # Token expires in 30 minutes
        'iat': datetime.utcnow(),
        'sub': identity,
        'rolName': rolName,
        'email': email
    }
    token = jwt.encode(payload, config('JWT_SECRET_KEY'), algorithm='HS256')
    return token

def validate_jwt(token):
    """
    Validate a JSON Web Token (JWT) and return the payload
    """
    try:
        payload = jwt.decode(token, config('JWT_SECRET_KEY'), algorithms=['HS256'])
        return {
            'identity': payload['sub'],
            'rolName': payload.get('rolName'),
            'email': payload.get('email')
        }
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_jwt_identity(token):
    """
    Get the identity from a valid JWT
    """
    payload = jwt.decode(token, config('JWT_SECRET_KEY'), algorithms=['HS256'])
    return payload['sub']
