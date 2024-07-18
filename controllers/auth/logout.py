from flask_restful import Resource, reqparse
from models.auth.logout import LogoutModel
from utils.server_response import StatusCode, ServerResponse
from utils.auth_manager import auth_required
from models.auth.db_queries import __dbmanager__

class LogoutController(Resource):
    route = '/auth/logout'

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help="Email cannot be blank!")
        args = parser.parse_args()

        email = args['email']

        user = LogoutModel.find_by_email(email)

        if not user:
            return ServerResponse(message="The user does not exist", message_code="INVALID_CREDENTIALS", status=StatusCode.BAD_REQUEST)
        
        LogoutModel.logout_user(email)

        return {
            'message': "User has been logged out",
            'message_code': "USER_LOGGED_OUT"
        }, StatusCode.OK
