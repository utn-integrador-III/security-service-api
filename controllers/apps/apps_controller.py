# controllers/apps/apps_controller.py
import logging
from flask import request
from flask_restful import Resource
from utils.server_response import ServerResponse, StatusCode
from models.apps.app import AppModel

class AppsListController(Resource):
    route = '/apps'

    def post(self):
        try:
            data = request.get_json(force=True, silent=True) or {}
            name = data.get('name')
            redirect_url = data.get('redirect_url')
            status = data.get('status', 'active')
            admin_id = data.get('admin_id')  # string -> se convertirá a ObjectId en el modelo

            if not all([name, redirect_url]):
                return ServerResponse(
                    message="Fields 'name' and 'redirect_url' are required.",
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            try:
                created = AppModel.create(name, redirect_url, status, admin_id)
                return ServerResponse(data=created, message="app created", status=StatusCode.CREATED).to_response()
            except ValueError as ve:
                return ServerResponse(message=str(ve), status=StatusCode.UNPROCESSABLE_ENTITY).to_response()
            except Exception as e:
                logging.error(f"Error creating app: {str(e)}", exc_info=True)
                return ServerResponse(message="Error creating app", status=StatusCode.INTERNAL_SERVER_ERROR).to_response()

        except Exception as e:
            logging.error(f"Unexpected error in POST /apps: {str(e)}", exc_info=True)
            return ServerResponse(message="An unexpected error occurred.", status=StatusCode.INTERNAL_SERVER_ERROR).to_response()

    def get(self):
        try:
            status = request.args.get('status')
            if status and status not in ('active', 'inactive'):
                return ServerResponse(
                    message="Invalid status. Allowed: 'active' | 'inactive'",
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            data = AppModel.list(status)
            return ServerResponse(data=data, status=StatusCode.OK).to_response()
        except Exception as e:
            logging.error(f"Unexpected error in GET /apps: {str(e)}", exc_info=True)
            return ServerResponse(message="An unexpected error occurred.", status=StatusCode.INTERNAL_SERVER_ERROR).to_response()


class AppsItemController(Resource):
    route = '/apps/<string:id>'

    def get(self, id):
        try:
            app = AppModel.get(id)
            if not app:
                return ServerResponse(message="app not found", status=StatusCode.NOT_FOUND).to_response()
            return ServerResponse(data=app, status=StatusCode.OK).to_response()
        except Exception as e:
            logging.error(f"Unexpected error in GET /apps/{id}: {str(e)}", exc_info=True)
            return ServerResponse(message="An unexpected error occurred.", status=StatusCode.INTERNAL_SERVER_ERROR).to_response()

    def patch(self, id):
        try:
            data = request.get_json(force=True, silent=True) or {}
            status = data.get('status')
            redirect_url = data.get('redirect_url')

            if status is None and redirect_url is None:
                return ServerResponse(
                    message="At least one of 'status' or 'redirect_url' must be provided.",
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            try:
                updated = AppModel.update(id, status=status, redirect_url=redirect_url)
            except ValueError as ve:
                return ServerResponse(message=str(ve), status=StatusCode.UNPROCESSABLE_ENTITY).to_response()

            if not updated:
                return ServerResponse(message="app not found", status=StatusCode.NOT_FOUND).to_response()

            return ServerResponse(message="app updated", data=updated, status=StatusCode.OK).to_response()
        except Exception as e:
            logging.error(f"Unexpected error in PATCH /apps/{id}: {str(e)}", exc_info=True)
            return ServerResponse(message="An unexpected error occurred.", status=StatusCode.INTERNAL_SERVER_ERROR).to_response()

    def delete(self, id):
        try:
            updated = AppModel.soft_delete(id)
            if not updated:
                return ServerResponse(message="app not found", status=StatusCode.NOT_FOUND).to_response()
            return ServerResponse(message="app inactivated", data=updated, status=StatusCode.OK).to_response()
        except Exception as e:
            logging.error(f"Unexpected error in DELETE /apps/{id}: {str(e)}", exc_info=True)
            return ServerResponse(message="An unexpected error occurred.", status=StatusCode.INTERNAL_SERVER_ERROR).to_response()
