from flask import Flask
from swagger_ui import flask_api_doc
from flask_restful import Api
from flask_cors import CORS
from decouple import config
from service import addServiceLayer
import logging

# ✅ Corrección en la importación
from controllers.user.security_user_enrollment import register_security_user
from controllers.rol.rol_controller import RolController

app = Flask(__name__)
app.debug = config('FLASK_DEBUG', cast=bool)
api = Api(app)
flask_api_doc(app, config_path='./swagger.yml', url_prefix='/api/doc', title='API doc')
logging.basicConfig(level=logging.INFO)

if config('SECURITY_API_ENVIRONMENT') == 'Development':
    cors = CORS(app, resources={r"/api/openapi": {"origins": "*"}, r"/*": {"origins": "*"}})

addServiceLayer(api)

@app.route('/security-user/register', methods=['POST'])
def security_user_register():
    return register_security_user()

# Get user roles for a specific application
@app.route('/roleByUser/<string:email>/<string:app>', methods=['GET'])
def get_roles_by_user_and_app(email, app):
    return RolController.get_roles_by_user_and_app(email, app)

if __name__ == "__main__":
    app.run(host=config('FLASK_RUN_HOST'), port=config('SECURITY_SERVICE_PORT'))
