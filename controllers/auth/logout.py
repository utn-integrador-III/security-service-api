import logging
from flask_restful import Resource, reqparse
from models.user.user import UserModel
from utils.server_response import StatusCode

class LogoutController(Resource):
    route = '/auth/logout'

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help="Email cannot be blank!")
        args = parser.parse_args()

        email = args['email']

        if not isinstance(email, str) or '@' not in email:
            logging.warning(f"Invalid email format: {email}")
            return {
                'message': "Invalid email format",
                'message_code': "INVALID_EMAIL"
            }, StatusCode.BAD_REQUEST

        user = UserModel.find_by_email(email)
        if not user:
            logging.warning(f"User not found with email: {email}")
            return {
                'message': "The user does not exist",
                'message_code': "INVALID_CREDENTIALS"
            }, StatusCode.BAD_REQUEST

        try:
            UserModel.logout_user(email)
            return {
                'message': "User has been logged out",
                'message_code': "USER_LOGGED_OUT"
            }, StatusCode.OK
        except Exception as e:
            return {
                'message': "An error occurred during logout",
                'message_code': "LOGOUT_ERROR"
            }, StatusCode.INTERNAL_SERVER_ERROR
