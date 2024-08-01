import jwt
from datetime import datetime, timedelta
from decouple import config

def generate_jwt(identity):
    """
    Generate a JSON Web Token (JWT) for the given identity
    """
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=30),  # Token expires in 30 minutes
        'iat': datetime.utcnow(),
        'sub': identity
    }
    token = jwt.encode(payload, config('JWT_SECRET_KEY'), algorithm='HS256')
    return token

def validate_jwt(token):
    """
    Validate a JSON Web Token (JWT)
    """
    try:
        payload = jwt.decode(token, config('JWT_SECRET_KEY'), algorithms=['HS256'])

        return payload['sub'], payload['exp']
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
