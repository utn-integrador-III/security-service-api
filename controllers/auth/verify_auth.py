from flask_restful import Resource, reqparse
from models.auth.auth import UserModel
from utils.server_response import StatusCode, ServerResponse
from utils.auth_manager import auth_required
import requests
from decouple import config
from flask import request
from utils.jwt_manager import validate_jwt, get_jwt_identity
class AuthController(Resource):
    route = '/auth/verify_auth'

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('permission', type=str, required=True, help='Permission is required')
        args = parser.parse_args()

        permission = args['permission']
        token = request.headers["Authorization"]
        
        # Validate JWT
        roles = validate_jwt(token)

        if roles is None:
            return ServerResponse(message="User Not valid", message_code="USER_NOT_FOUND", status=StatusCode.BAD_REQUEST)


        body= {'name': roles}
        response = requests.get(config('AUTH_API_URL') + config('AUTH_API_PORT') + '/role', json=body)
        
        return {
            'data': {
                "rol": response['name'],
                "permissions": response['permissions'],
                "screens": response['screens']
            },
            'message': "User has been authenticated",
            'message_code': "USER_AUTHENTICATED"
        }, StatusCode.OK