from flask_restful import Resource, reqparse
from utils.server_response import StatusCode, ServerResponse
from utils.jwt_manager import validate_jwt
from flask import request

class AuthController(Resource):
    route = '/auth/verify_auth'

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('permission', type=str, required=False, help='Permission is optional')
        args = parser.parse_args()

        permission = args.get('permission')
        token = request.headers.get("Authorization")

        if not token:
            return ServerResponse(
                data=None,
                message="Authorization token is required",
                message_code="AUTH_TOKEN_REQUIRED",
                status=StatusCode.UNAUTHORIZED
            ).to_response()

        # Validate JWT
        user_data = validate_jwt(token)

        if user_data is None:
            return ServerResponse(
                message="Invalid or expired token",
                message_code="INVALID_TOKEN",
                status=StatusCode.UNAUTHORIZED
            ).to_response()

        if permission:
            if not self.has_permission(user_data, permission):
                return ServerResponse(
                    message="Permission denied",
                    message_code="PERMISSION_DENIED",
                    status=StatusCode.FORBIDDEN
                ).to_response()

        return ServerResponse(
            data=user_data,
            message="User is valid",
            message_code="USER_AUTHENTICATED",
            status=StatusCode.OK
        ).to_response()

    def has_permission(self, user_data, permission):
        user_permissions = user_data.get('permissions', [])
        return permission in user_permissions
