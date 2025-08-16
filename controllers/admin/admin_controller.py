# controllers/admin/admin_controller.py
import logging
from flask import request
from flask_restful import Resource
from validate_email import validate_email
from utils.server_response import ServerResponse, StatusCode
from models.admin.admin import AdminModel

class AdminListController(Resource):
    route = '/admin'

    def post(self):
        try:
            data = request.get_json(force=True, silent=True) or {}
            admin_email = data.get('admin_email')
            password = data.get('password')
            status = data.get('status', 'active')

            # Validaciones mínimas 
            if not all([admin_email, password]):
                return ServerResponse(
                    message="Fields 'admin_email' and 'password' are required.",
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            if not validate_email(admin_email):
                return ServerResponse(
                    message="The provided email is not valid",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            if not isinstance(password, str) or len(password) < 8:
                return ServerResponse(
                    message="The password must be at least 8 characters long.",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            if status not in ('active', 'inactive'):
                return ServerResponse(
                    message="Invalid status. Allowed: 'active' | 'inactive'",
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            try:
                created = AdminModel.create(admin_email, password, status)
                return ServerResponse(
                    data=created,
                    message="admin created",
                    status=StatusCode.CREATED
                ).to_response()
            except ValueError as ve:  
                return ServerResponse(
                    message=str(ve),
                    status=StatusCode.CONFLICT
                ).to_response()
            except Exception as e:
                logging.error(f"Error creating admin: {str(e)}", exc_info=True)
                return ServerResponse(
                    message="Error creating admin",
                    status=StatusCode.INTERNAL_SERVER_ERROR
                ).to_response()

        except Exception as e:
            logging.error(f"An unexpected error occurred in POST /admin: {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()

    def get(self):
        try:
            status = request.args.get('status')
            if status and status not in ('active', 'inactive'):
                return ServerResponse(
                    message="Invalid status. Allowed: 'active' | 'inactive'",
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            data = AdminModel.list(status)
            return ServerResponse(
                data=data,
                status=StatusCode.OK
            ).to_response()
        except Exception as e:
            logging.error(f"Unexpected error in GET /admin: {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()


class AdminItemController(Resource):
    route = '/admin/<string:id>'

    def get(self, id):
        try:
            admin = AdminModel.get(id)
            if not admin:
                return ServerResponse(
                    message="admin not found",
                    status=StatusCode.NOT_FOUND
                ).to_response()
            return ServerResponse(
                data=admin,
                status=StatusCode.OK
            ).to_response()
        except Exception as e:
            logging.error(f"Unexpected error in GET /admin/{id}: {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()

    def patch(self, id):
        try:
            data = request.get_json(force=True, silent=True) or {}
            status = data.get('status')
            new_password = data.get('password')

            if status and status not in ('active', 'inactive'):
                return ServerResponse(
                    message="Invalid status. Allowed: 'active' | 'inactive'",
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            if new_password is not None and len(str(new_password)) < 8:
                return ServerResponse(
                    message="The password must be at least 8 characters long.",
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            updated = AdminModel.update(id, status=status, new_password=new_password)
            if not updated:
                return ServerResponse(
                    message="admin not found",
                    status=StatusCode.NOT_FOUND
                ).to_response()

            return ServerResponse(
                message="admin updated",
                data=updated,
                status=StatusCode.OK
            ).to_response()
        except Exception as e:
            logging.error(f"Unexpected error in PATCH /admin/{id}: {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()

    def delete(self, id):
        try:
            updated = AdminModel.soft_delete(id)
            if not updated:
                return ServerResponse(
                    message="admin not found",
                    status=StatusCode.NOT_FOUND
                ).to_response()
            return ServerResponse(
                message="admin inactivated",
                data=updated,
                status=StatusCode.OK
            ).to_response()
        except Exception as e:
            logging.error(f"Unexpected error in DELETE /admin/{id}: {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()
