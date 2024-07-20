from flask_restful import Resource, reqparse
from models.auth.auth import UserModel
from utils.server_response import StatusCode, ServerResponse
from utils.jwt_manager import validate_jwt
from flask import request

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
            return ServerResponse(message="User Not valid", message_code="USER_NOT_FOUND", status=StatusCode.BAD_REQUEST).to_response()
        
        return ServerResponse(
            data={"rolName": roles},
            message="User is valid",
            message_code="USER_AUTHENTICATED",
            status=StatusCode.OK
        ).to_response()
