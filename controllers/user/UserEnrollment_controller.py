import logging
import random
from datetime import datetime, timedelta
from flask import request
from flask_restful import Resource
from validate_email import validate_email
from models.user.user import UserModel
from models.role.role import RoleModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import (
INVALID_EMAIL_DOMAIN, INVALID_NAME, INVALID_PASSWORD, USER_ALREADY_REGISTERED, USER_SUCCESSFULLY_CREATED, INVALID_ROLE  # Ensure this is defined somewhere in your utils.message_codes
)

class UserEnrollmentController(Resource):
    route = '/user/enrollment'
    
    def post(self):
        try:
            data = request.json
            name = data.get('name')
            password = data.get('password')
            email = data.get('email')
            provided_roles = data.get('roles', [])
            
            # Validate email
            if not email or not validate_email(email):
                return ServerResponse(
                    message="The provided email is not valid",
                    message_code=INVALID_EMAIL_DOMAIN,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()
            
            if not any(domain in email for domain in ['utn.ac.cr', 'est.utn.ac.cr', 'adm.utn.ac.cr']):
                return ServerResponse(
                    message="The entered domain does not meet the established standards",
                    message_code=INVALID_EMAIL_DOMAIN,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()
            
            # Validate name
            if not name or len(name.strip()) < 2:
                return ServerResponse(
                    message="The name does not meet the established standards",
                    message_code=INVALID_NAME,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()
            
            # Validate password
            if not password or len(password) < 8:
                return ServerResponse(
                    message="The password does not meet the established standards",
                    message_code=INVALID_PASSWORD,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()
            
            # Check if user already exists
            existing_user = UserModel.find_by_email(email)
            if existing_user:
                return ServerResponse(
                    message="The user is already registered",
                    message_code=USER_ALREADY_REGISTERED,
                    status=StatusCode.CONFLICT
                ).to_response()
                
            # Fetch active roles
            active_roles = RoleModel.find_active_roles()
            if not active_roles:
                return ServerResponse(
                    message="No active roles found",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()
            
            valid_role_names = [role.get('name', '').lower().strip() for role in active_roles]
            if not valid_role_names:
                return ServerResponse(
                    message="No valid role names found",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()
            
            # Validate provided roles
            invalid_roles = [role for role in provided_roles if role.lower().strip() not in valid_role_names]
            if invalid_roles:
                return ServerResponse(
                    message=f"The following roles are not valid: {', '.join(invalid_roles)}",
                    message_code=INVALID_ROLE,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()
                
            # Use default roles if none provided
            if not provided_roles:
                default_roles = [role for role in active_roles if role.get('default_role', False)]
                provided_roles = [role.get('name') for role in default_roles]
            
            # Generate verification code and expiration code
            verification_code = random.randint(100000, 999999)
            expiration_code = datetime.utcnow() + timedelta(minutes=5)
            
            # Create new user
            user_data = {
                'name': name,
                'password': password,
                'email': email,
                'status': 'Pending',
                'verification_code': verification_code,
                'expiration_code': expiration_code,
                'roles': provided_roles,
                'token': "",
                'is_session_active': False
            }
            
            new_user = UserModel.create_user(user_data)
            
            return ServerResponse(
                message="User successfully created",
                message_code=USER_SUCCESSFULLY_CREATED,
                status=StatusCode.OK
            ).to_response()
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()
