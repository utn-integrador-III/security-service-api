from flask_restful import Resource
from utils.server_response import StatusCode, ServerResponse
from utils.jwt_manager import validate_jwt, generate_jwt
from datetime import datetime, timedelta
from flask import request

class RefreshController(Resource):
    route = '/auth/refresh'
    
    def post(self):
        # Extract the token directly from the header without checking for "Bearer " prefix
        token = request.headers.get("Authorization")
        if not token:
            return ServerResponse(
                message="Token not added",
                message_code="BAD_REQUEST",
                status=StatusCode.BAD_REQUEST
            ).to_response()

        # Validate the old token
        result = validate_jwt(token)
        if result is None:
            return ServerResponse(
                message="Token Not Valid",
                message_code="NOT_FOUND",
                status=StatusCode.NOT_FOUND
            ).to_response()

        # Extract details from the validated token
        subject = result['identity']
        role_name = result['rolName']
        email = result['email']
        name = result['name']
        status = result['status']
        expiration_time = result.get('exp', datetime.utcnow())  # Ensure expiration time is available
        current_time = datetime.utcnow()
        grace_period_end = expiration_time + timedelta(minutes=30)  # Grace period for token refresh

        # Check if the token is expired
        if current_time > expiration_time:
            if current_time < grace_period_end:
                # If within grace period, issue a new token
                new_token = generate_jwt(subject, role_name, email, name, status)
                return ServerResponse(
                    data={'token': new_token},
                    message='Token Refreshed',
                    message_code='OK',
                    status=StatusCode.OK
                ).to_response()
            else:
                # Token is beyond the grace period
                return ServerResponse(
                    message="Token Expired",
                    message_code="UNAUTHORIZED",
                    status=StatusCode.UNAUTHORIZED
                ).to_response()
        else:
            # Token not expired, issue a new one anyway for refresh
            new_token = generate_jwt(subject, role_name, email, name, status)
            return ServerResponse(
                data={'token': new_token},
                message='Token Refreshed',
                message_code='OK',
                status=StatusCode.OK
            ).to_response()
