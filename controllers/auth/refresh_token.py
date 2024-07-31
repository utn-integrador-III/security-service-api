from flask_restful import Resource, reqparse
from utils.server_response import StatusCode, ServerResponse
from utils.jwt_manager import validate_jwt, generate_jwt
from datetime import datetime, timedelta
from flask import request

class RefreshController(Resource):
    route = '/refresh'
    def post(self):
        # Extract the token from the request headers or body
        token = request.headers["Authorization"]
        if not token:
            return ServerResponse(message="Token not added", message_code="BAD_REQUEST", status=StatusCode.BAD_REQUEST).to_response()

        # Validate the old token but ignore expiration error
        payload = validate_jwt(token)
        if not payload:
            return ServerResponse(message="Token Not Valid", message_code="NOT_FOUND", status=StatusCode.NOT_FOUND).to_response()

        # Check if the token is expired
        if 'exp' in payload:
            expiration_time = datetime.utcfromtimestamp(payload['exp'])
            if expiration_time < datetime.utcnow():
                # Token is expired, check if it's within a grace period
                grace_period = datetime.utcnow() + timedelta(minutes=5)  # 5 minutes grace period
                if expiration_time < grace_period:
                    # If within grace period, issue a new token
                    new_token = generate_jwt(payload['sub'])
                    return ServerResponse(
                        data={'token': new_token},
                        message='Token Refreshed',
                        message_code='OK',
                        status=StatusCode.OK,
                    ).to_response()
                else:
                    return ServerResponse(message="Token Expired", message_code="UNAUTHORIZED", status=StatusCode.UNAUTHORIZED).to_response()
            else:
                # Token not expired, issue a new one
                new_token = generate_jwt(payload['sub'])
                return ServerResponse(
                        data={'token': new_token},
                        message='Token Refreshed',
                        message_code='OK',
                        status=StatusCode.OK,
                    ).to_response()

        return ServerResponse(message="Internal Server Error", message_code="INTERNAL_SERVER_ERROR", status=StatusCode.INTERNAL_SERVER_ERROR).to_response()
