from flask import Response
import json
import logging

class StatusCode:
    # Status codes
    OK = 200
    CREATED = 201
    NOT_FOUND = 404
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    INTERNAL_SERVER_ERROR = 500
    TIMEOUT = 503
    BAD_REQUEST = 400
    FORBIDDEN = 403 
    UNAUTHORIZED = 401

class ServerResponse:
    """Handle server responses
    
    Keyword arguments:
    data -- values returned
    message -- description of the response
    message_code -- multilanguage code 
    status -- integer http status code
    """
    def __init__(self, data=None, message=None, message_code=None, status=StatusCode.OK):
        self.data = data
        self.message = message
        self.message_code = message_code
        self.status = status
        self.__get_default_msg()

    def __get_default_msg(self):
        if not self.message:
            if self.status == StatusCode.OK:
                self.message = 'Successfully requested'
                self.message_code = "OK_MSG"
            elif self.status == StatusCode.CREATED:
                self.message = 'Successfully created'
                self.message_code = "CREATED_MSG"
            elif self.status == StatusCode.NOT_FOUND:
                self.message = 'Record not found'
                self.message_code = "NOT_FOUND_MSG"
            elif self.status == StatusCode.CONFLICT:
                self.message = 'Conflict error with the request'
                self.message_code = "CONFLICT_MSG"
            elif self.status == StatusCode.UNPROCESSABLE_ENTITY:
                self.message = 'Unprocessable entity'
                self.message_code = "UNPROCESSABLE_ENTITY_MSG"
            elif self.status == StatusCode.INTERNAL_SERVER_ERROR:
                self.message = 'Internal server error'
                self.message_code = "INTERNAL_SERVER_ERROR_MSG"
            elif self.status == StatusCode.TIMEOUT:
                self.message = 'Server timeout'
                self.message_code = "SERVER_TIMEOUT_MSG"

    def __server_response(self):
        self.__get_default_msg()
        body = {
            'data': self.data,
            'message': self.message,
            'message_code': self.message_code
        }
        try:
            body_json = json.dumps(body, default=str)  # Use default=str to handle datetime serialization
        except TypeError as e:
            logging.error(f"Serialization error: {e}")
            body_json = json.dumps({'message': 'Serialization error'}, default=str)
        return Response(body_json, mimetype='application/json', status=int(self.status))

    def to_response(self):
        return self.__server_response()
