from flask_restful import Resource, reqparse
from models.auth.auth import UserModel
from utils.server_response import StatusCode, ServerResponse
from utils.auth_manager import auth_required
from utils.jwt_manager import generate_jwt

class LoginController(Resource):
    route = '/auth/login'

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help="Email cannot be blank!")
        parser.add_argument('password', required=True, help="Password cannot be blank!")
        args = parser.parse_args()

        email = args['email']
        password = args['password']

        # Validar dominios de correo electrónico permitidos
        allowed_domains = ["@utn.ac.cr", "@est.utn.ac.cr"]
        if not any(email.endswith(domain) for domain in allowed_domains):
            return ServerResponse(message="Invalid email domain", message_code="INVALID_EMAIL_DOMAIN", status=StatusCode.BAD_REQUEST)

        user = UserModel.find_by_email(email)

        if not user:
            return ServerResponse(message="Invalid email or password", message_code="INVALID_CREDENTIALS", status=StatusCode.BAD_REQUEST)

        if not UserModel.verify_password(password, user['password']):
            return ServerResponse(message="Invalid email or password", message_code="INVALID_CREDENTIALS", status=StatusCode.BAD_REQUEST)

        if user['status'] != "Active":
            return ServerResponse(message="User is not active", message_code="USER_NOT_ACTIVE", status=StatusCode.BAD_REQUEST)

        # Generar el JWT
        token = generate_jwt(user['roles'])
        
        return {
            'data': {
                "email": user['email'],
                "name": user['name'],
                "status": user['status'],
                "role_id": user['roles'],
                "token": token
            },
            'message': "User has been authenticated",
            'message_code': "USER_AUTHENTICATED"
        }, StatusCode.OK