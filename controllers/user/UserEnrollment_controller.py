import logging
import random
from datetime import datetime, timedelta
from flask import request, Response
from flask_restful import Resource
from validate_email import validate_email
from models.user.user import UserModel
from models.role.role import RoleModel
from utils.email_manager import send_email
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import (
    CREATED, INVALID_EMAIL_DOMAIN, INVALID_NAME, INVALID_PASSWORD, USER_ALREADY_REGISTERED, NO_ACTIVE_ROLES_FOUND, DEFAULT_ROLE_NOT_FOUND, USER_CREATION_ERROR, UNEXPECTED_ERROR
)

class UserEnrollmentController(Resource):
    route = '/user/enrollment'

    def post(self):
        try:
            data = request.json
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            apps_data = data.get('apps', [])

            # Validate required fields
            if not all([name, email, password]) or not apps_data:
                return ServerResponse(
                    message="Fields 'name', 'email', 'password', and at least one 'app' are required.",
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            # Validate email
            if not email or not validate_email(email):
                return ServerResponse(
                    message="The provided email is not valid",
                    message_code=INVALID_EMAIL_DOMAIN,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()
            
            # Validate specific domain required for email
            """if not any(domain in email for domain in ['utn.ac.cr', 'est.utn.ac.cr', 'adm.utn.ac.cr']):
                return ServerResponse(
                    message="The entered domain does not meet the established standards",
                    message_code=INVALID_EMAIL_DOMAIN,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()"""

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

            try:
                # Search if the user already exists
                existing_user = UserModel.find_by_email(email)

                # Generate code and expiration for each app
                for app in apps_data:
                    app["code"] = str(random.randint(100000, 999999))
                    app["token"] = ""
                    app["status"] = "Pending"
                    expiration_code = datetime.utcnow() + timedelta(minutes=5)
                    app["code_expliration"] = expiration_code.strftime("%Y/%m/%d %H:%M:%S")

                if existing_user:
                    user_apps = existing_user.get("apps", [])
                    updated = False

                    for new_app in apps_data:
                        already_exists = any(
                            app["role"] == new_app["role"] and app["app"] == new_app["app"]
                            for app in user_apps
                        )
                        if already_exists:
                            return ServerResponse(
                                message=f"User already assigned to role '{new_app['role']}' and app '{new_app['app']}'.",
                                status=StatusCode.CONFLICT
                            ).to_response()
                        else:
                            user_apps.append(new_app)
                            updated = True
                            send_email(email, new_app["code"])

                    if updated:
                        update_data = {
                            "apps": user_apps,
                            "status": "Pending"
                        }
                        UserModel.update_user(email, update_data)

                        return ServerResponse(
                            data=None,
                            message="User updated with new role(s) and app(s). Verification code(s) sent.",
                            message_code=CREATED,
                            status=StatusCode.OK
                        ).to_response()

                # Create new user with complete structure
                user_data = {
                    "name": name,
                    "password": password,
                    "email": email,
                    "status": "Pending",
                    "apps": apps_data,
                    "is_session_active": False
                }

                UserModel.create_user(user_data)

                for app in apps_data:
                    send_email(email, app["code"])

                return ServerResponse(
                    data=None,
                    message="User created successfully and verification code(s) sent.",
                    message_code=CREATED,
                    status=StatusCode.CREATED
                ).to_response()

            except Exception as e:
                logging.error(f"Error creating user: {str(e)}", exc_info=True)
                return ServerResponse(
                    message="Error creating user",
                    message_code=USER_CREATION_ERROR,
                    status=StatusCode.INTERNAL_SERVER_ERROR
                ).to_response()

        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                message_code=UNEXPECTED_ERROR,
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()