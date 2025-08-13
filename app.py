from flask import Flask
from swagger_ui import flask_api_doc
from flask_restful import Api
from flask_cors import CORS
from decouple import config
from service import addServiceLayer
import logging


from controllers.user.security_user_enrollment import register_security_user
from controllers.rol.rol_controller import RolController
from controllers.rol.screnss_controller import ScreensController


app = Flask(__name__)
app.debug = config('FLASK_DEBUG', cast=bool)
api = Api(app)
flask_api_doc(app, config_path='./swagger.yml', url_prefix='/api/doc', title='API doc')
logging.basicConfig(level=logging.INFO)

if config('SECURITY_API_ENVIRONMENT') == 'Development':
    cors = CORS(app, resources={r"/api/openapi": {"origins": "*"}, r"/*": {"origins": "*"}})
addServiceLayer(api)

#Endpoint register user
@app.route('/security-user/register', methods=['POST'])
def security_user_register():
    return register_security_user()



##             ENDPOINT ROLE             ##

#Get one
@app.route('/roleByUser/<string:email>/<string:app>', methods=['GET'])
def get_roles_by_user_and_app(email, app):
    return RolController.get_roles_by_user_and_app(email, app)


#endpoint post of the role
@app.route('/role/<string:app_id>/create', methods=['POST'])
def post_role(app_id):
    return RolController.post(app_id)



#Endpoint delete rol
@app.route("/role/<app_id>/delete", methods=["DELETE"])
def delete_role(app_id):
    return RolController.delete(app_id)



# Endpoint update rol 
@app.route("/role/<app_id>/update", methods=["PUT"])
def update_role(app_id):
    return RolController.patch(app_id)


##             ENDPOINTS SCREENS            ##

#endpoint post of the screens rol
@app.route('/role/<string:client_id>/screens', methods=['POST'])
def post_screens(client_id):
    return ScreensController.post_add_screens(client_id)


@app.route('/role/<string:client_id>/screens/delete', methods=['DELETE'])
def delete_screens(client_id):
    return ScreensController.delete_screens(client_id)


@app.route('/role/<string:client_id>/screens', methods=['GET'])
def get_screens(client_id):
    return ScreensController.get_screens(client_id)





if __name__ == "__main__":
    app.run(host=config('FLASK_RUN_HOST'), port=config('SECURITY_SERVICE_PORT'))
