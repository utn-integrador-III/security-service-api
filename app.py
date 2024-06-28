from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from decouple import config
from service import addServiceLayer

app = Flask(__name__)
app.debug = config('FLASK_DEBUG', cast=bool)
api = Api(app)

if config('SECURITY_API_ENVIRONMENT') == 'Development':
    cors = CORS(app, resources={r"/api/openapi": {"origins": "*"}, r"/*": {"origins": "*"}})

addServiceLayer(api)

if __name__ == "__main__":
    app.run(host=config('FLASK_RUN_HOST'), port=config('SECURITY_SERVICE_PORT'))
