from flask_restful import Resource, reqparse
from models.auth.auth import UserModel

class AuthController(Resource):
    route = '/login'

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
            return {"message": "Invalid email domain", "message_code": "INVALID_EMAIL_DOMAIN"}, 400

        user = UserModel.find_by_email(email)

        if not user:
            return {"message": "Invalid email or password", "message_code": "INVALID_CREDENTIALS"}, 400

        if not UserModel.verify_password(password, user['password']):
            return {"message": "Invalid email or password", "message_code": "INVALID_CREDENTIALS"}, 400

        if user['status'] != "Active":
            return {"message": "User is not active", "message_code": "USER_NOT_ACTIVE"}, 400

        return {
            'data': {
                "email": user['email'],
                "name": user['name'],
                "status": user['status'],
                "role_id": user['roles'],
                "token": ""
            },
            'message': "User has been authenticated",
            'message_code': "USER_AUTHENTICATED"
        }, 200
