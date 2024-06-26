from flask import Flask
#from swagger_ui import flask_api_doc
from flask_restful import Api
from flask_cors import CORS
from decouple import config
from service import addServiceLayer
from controllers.user.user_controller import UserController
app = Flask(__name__)
app.debug = config('FLASK_DEBUG', cast=bool)
api = Api(app)
#flask_api_doc(app, config_path='./swagger.yml', url_prefix='/api/doc', title='API doc')
if config('SECURITY_API_ENVIRONMENT')=='Development':
    cors = CORS(app, resources={r"/api/openapi": {"origins": "*"}, r"/*": {"origins": "*"}})

addServiceLayer(api)

@app.route('/register', methods=['POST'])
def register_user():
    return UserController().post()

if __name__ == "__main__":
    app.run(host=config('FLASK_RUN_HOST'), port=config('SECURITY_SERVICE_PORT'))