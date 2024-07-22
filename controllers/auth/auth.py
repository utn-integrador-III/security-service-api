from flask_restful import Resource, reqparse
from models.user.user import UserModel
from utils.server_response import StatusCode, ServerResponse
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
            return ServerResponse(message="Invalid email domain", message_code="INVALID_EMAIL_DOMAIN", status=StatusCode.BAD_REQUEST).to_response()

        user = UserModel.find_by_email(email)

        if not user:
            print(user)
            return ServerResponse(message="Invalid email or password", message_code="INVALID_CREDENTIALS", status=StatusCode.BAD_REQUEST).to_response()      

        if not UserModel.verify_password(password, user['password']):
            return ServerResponse(message="Invalid email or password", message_code="INVALID_CREDENTIALS", status=StatusCode.BAD_REQUEST).to_response()

        if user['status'] != "Active":
            return ServerResponse(message="User is not active", message_code="USER_NOT_ACTIVE", status=StatusCode.BAD_REQUEST).to_response()

        # Generar el JWT
        token = generate_jwt(user['role'])
        
        response_data = {
            'data': {
                "email": user['email'],
                "name": user['name'],
                "status": user['status'],
                "role": user['role'],
                "token": token
            },
            'message': "User has been authenticated",
            'message_code': "USER_AUTHENTICATED"
        }

        return ServerResponse(
            data=response_data['data'],
            message=response_data['message'],
            message_code=response_data['message_code'],
            status=StatusCode.OK
        ).to_response()
