<<<<<<< HEAD
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
        try:
            # Check connection status
            info_db= HealthModel.getInfoDB()
            return ServerResponse(message='Connection to DB is OK',
                                        message_code=HEALTH_SUCCESSFULLY, status=StatusCode.OK)         
        except Exception as ex:
            print(ex)
            logging.exception(ex)
            return ServerResponse(message='Connection to DB is not possible.',
=======
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
        try:
            # Check connection status
            info_db= HealthModel.getInfoDB()
            return ServerResponse(message='Connection to DB is OK',
                                        message_code=HEALTH_SUCCESSFULLY, status=StatusCode.OK)         
        except Exception as ex:
            print(ex)
            logging.exception(ex)
            return ServerResponse(message='Connection to DB is not possible.',
>>>>>>> 3700107 (Document the endpoint to enroll a new user. In swagger.yml add the endpoint inside Auth section & the existing endpoint with the path /register was changed to the correct /auth/enrollment)
                                      message_code=HEALTH_NOT_FOUND, status=StatusCode.NOT_FOUND)