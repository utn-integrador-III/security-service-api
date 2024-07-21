from flask_restful import Resource
from utils.server_response import ServerResponse, StatusCode
from models.role.role import RoleModel
from .parser import RolParser
import logging

class RolController(Resource):
    route = "/rol"

    """
    Get a rol
    """
    def get(self):
        try:
            arg = RolParser.parse_put_request()
            object_name = arg['name']

            if not object_name:
                response = ServerResponse(message="name not inserted", message_code="ROL_NOT_FOUND", status=StatusCode.NOT_FOUND)
                return response.to_response()
            
            result = RoleModel.get_by_name(object_name)
            
            if isinstance(result, dict) and "error" in result:
                response = ServerResponse(
                    data={},
                    message=result["error"],
                    status=StatusCode.INTERNAL_SERVER_ERROR,
                )
                return response.to_response()

            if not result:  # If there are no rol objects
                response = ServerResponse(
                    data={},
                    message="No rol objects found",
                    message_code="NO_DATA",
                    status=StatusCode.OK,
                )
                return response.to_response()
            else:
                response = ServerResponse(
                    data=result.to_dict(),  # Convert the RolModel instance to a dictionary
                    message="ROL_FOUND",
                    message_code="OK_MSG",
                    status=StatusCode.OK,
                )
                return response.to_response()
        except Exception as ex:
            logging.error(ex)
            response = ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
            return response.to_response()
