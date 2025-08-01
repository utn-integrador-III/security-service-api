import logging
from flask import request
from flask_restful import Resource
from models.application.application import ApplicationModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import CREATED, INVALID_NAME, USER_ALREADY_REGISTERED, UNEXPECTED_ERROR, INVALID_EMAIL_DOMAIN, INVALID_URL
from validate_email import validate_email
import re

def is_valid_url(url):
    # Simple regex for URL validation
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

class ApplicationRegistrationController(Resource):
    route = '/application/register'

    def post(self):
        try:
            data = request.json
            name = data.get('name')
            admin_email = data.get('admin_email')
            redirect_url = data.get('redirect_url')

            # Validations
            if not name or len(name.strip()) < 2:
                return ServerResponse(message="Invalid application name", message_code=INVALID_NAME, status=StatusCode.UNPROCESSABLE_ENTITY).to_response()

            if not admin_email or not validate_email(admin_email):
                return ServerResponse(message="Invalid admin email", message_code=INVALID_EMAIL_DOMAIN, status=StatusCode.UNPROCESSABLE_ENTITY).to_response()

            if not redirect_url or not is_valid_url(redirect_url):
                 return ServerResponse(message="Invalid redirect URL", message_code=INVALID_URL, status=StatusCode.UNPROCESSABLE_ENTITY).to_response()

            app_model = ApplicationModel()

            # Check if application already exists
            if app_model.find_by_name(name):
                return ServerResponse(message="Application already registered", message_code=USER_ALREADY_REGISTERED, status=StatusCode.CONFLICT).to_response()

            # Create application
            new_app_credentials = app_model.create_application(data)

            if not new_app_credentials:
                return ServerResponse(message="Error creating application", status=StatusCode.INTERNAL_SERVER_ERROR).to_response()

            return ServerResponse(
                data=new_app_credentials,
                message="Application registered successfully",
                message_code=CREATED,
                status=StatusCode.CREATED
            ).to_response()

        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
            return ServerResponse(message="An unexpected error occurred", message_code=UNEXPECTED_ERROR, status=StatusCode.INTERNAL_SERVER_ERROR).to_response()
