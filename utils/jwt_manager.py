import jwt
from datetime import datetime, timedelta
from decouple import config

def generate_jwt(identity, rolName, email, name, status):
    """
    Generate a JSON Web Token (JWT) for the given identity with additional details
    """
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=30), 
        'iat': datetime.utcnow(),
        'sub': identity,
        'rolName': rolName,
        'email': email,
        'name': name,
        'status': status
    }
    token = jwt.encode(payload, config('JWT_SECRET_KEY'), algorithm='HS256')
    return token

def validate_jwt(token):
    """
    Validate a JSON Web Token (JWT) and return the payload
    """
    try:
        token = token.replace("Bearer", "").strip()  # Remove 'Bearer' prefix if present
        payload = jwt.decode(token, config('JWT_SECRET_KEY'), algorithms=['HS256'])
        return {
            'identity': payload['sub'],
            'rolName': payload.get('rolName'),
            'email': payload.get('email'),
            'name': payload.get('name'),
            'status': payload.get('status') 
        }
    except jwt.ExpiredSignatureError:
        print("JWT has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid JWT token")
        return None

def get_jwt_identity(token):
    """
    Get the identity from a valid JWT
    """
    payload = jwt.decode(token, config('JWT_SECRET_KEY'), algorithms=['HS256'])
    return payload['sub']
