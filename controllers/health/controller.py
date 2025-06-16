from flask_restful import Resource

from utils.server_response import *
from utils.message_codes import *
from models.health.model import HealthModel
import logging


class HealthController(Resource):
    route = '/health'

    """
    Get heath
    """
    def get(self):
        response=None
        try:
            # Check connection status
            info_db= HealthModel.getInfoDB()
            response = ServerResponse(message='Connection to DB is OK',
                                        message_code=HEALTH_SUCCESSFULLY, status=StatusCode.OK)      
        except Exception as ex:
            print(ex)
            logging.exception(ex)
            response = ServerResponse(message='Connection to DB is not possible.',
                                      message_code=HEALTH_NOT_FOUND, status=StatusCode.NOT_FOUND)
        return response.to_response()