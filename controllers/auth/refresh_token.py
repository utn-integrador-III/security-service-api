from flask_restful import Resource, reqparse
from utils.server_response import StatusCode, ServerResponse
from utils.jwt_manager import validate_jwt, generate_jwt
from datetime import datetime, timedelta
from flask import request

class RefreshController(Resource):
    route = '/auth/refresh'
    def post(self):
        # Extract the token from the request headers or body
        token = request.headers.get("Authorization")
        if not token:
            return ServerResponse(message="Token not added", message_code="BAD_REQUEST", status=StatusCode.BAD_REQUEST).to_response()

        # Validate the old token but ignore expiration error
        subject, exp_timestamp = validate_jwt(token)
        if subject is None:
            return ServerResponse(message="Token Not Valid", message_code="NOT_FOUND", status=StatusCode.NOT_FOUND).to_response()

        # Check if the token is expired
        expiration_time = datetime.utcfromtimestamp(exp_timestamp)
        current_time = datetime.utcnow()
        grace_period_end = expiration_time + timedelta(minutes=5)  # 5 minutes grace period after expiration

        if current_time > expiration_time:
            if current_time < grace_period_end:
                # If within grace period, issue a new token
                new_token = generate_jwt(subject)
                return ServerResponse(
                    data={'token': new_token},
                    message='Token Refreshed',
                    message_code='OK',
                    status=StatusCode.OK,
                ).to_response()
            else:
                # Token is beyond the grace period
                return ServerResponse(message="Token Expired", message_code="UNAUTHORIZED", status=StatusCode.UNAUTHORIZED).to_response()
        else:
            # Token not expired, issue a new one anyway for refresh
            new_token = generate_jwt(subject)
            return ServerResponse(
                    data={'token': new_token},
                    message='Token Refreshed',
                    message_code='OK',
                    status=StatusCode.OK,
                ).to_response()
