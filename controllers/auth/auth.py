# controllers/login_controller.py
from flask_restful import Resource, reqparse
from models.user.user import UserModel
from utils.server_response import StatusCode, ServerResponse
from utils.jwt_manager import generate_jwt
from utils.email_validator import is_valid_email_domain
from models.role.role import RoleModel

class LoginController(Resource):
    route = '/auth/login'

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', required=True, help="Email cannot be blank!")
        self.parser.add_argument('password', required=True, help="Password cannot be blank!")

    def post(self):
        args = self.parser.parse_args()
        email = args['email']
        password = args['password']

        if not is_valid_email_domain(email):
            return ServerResponse(
                message="Invalid email domain",
                message_code="INVALID_EMAIL_DOMAIN",
                status=StatusCode.BAD_REQUEST
            ).to_response()

        user = UserModel.find_by_email(email)

        if not user or not UserModel.verify_password(password, user['password']):
            return ServerResponse(
                message="Invalid email or password",
                message_code="INVALID_CREDENTIALS",
                status=StatusCode.UNAUTHORIZED
            ).to_response()

        if user['status'] != "Active":
            return ServerResponse(
                message="User is not active",
                message_code="USER_NOT_ACTIVE",
                status=StatusCode.FORBIDDEN
            ).to_response()

        token = generate_jwt(user['role'])
        
        # Update user's token in the database
        success = UserModel.update_token(user['id'], token)
        if not success:
            return ServerResponse(
                message="Failed to update user token",
                message_code="TOKEN_UPDATE_FAILED",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()
        
        role_object = RoleModel.get_by_name(user['role'])
        filtered_role_data = {
        "name": role_object.name,
        "permissions": role_object.permissions,
        "is_active": role_object.is_active,
        "screens": role_object.screens
    }

        response_data = {
            'data': {
                "email": user['email'],
                "name": user['name'],
                "status": user['status'],
                "role": filtered_role_data,
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
