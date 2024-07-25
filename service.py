# app.py o service.py
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from controllers.health.controller import HealthController
from controllers.auth.auth import AuthController
from controllers.user.UserEnrollment_controller import UserEnrollmentController
from controllers.auth.VerifyCodeController import VerifyCodeController

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Habilita CORS en tu aplicación Flask
api = Api(app)

def addServiceLayer(api: Api):
    # Health
    api.add_resource(HealthController, HealthController.route)
    
    # Auth
    api.add_resource(AuthController, AuthController.route)
    
    # User
    api.add_resource(UserEnrollmentController, UserEnrollmentController.route)
    
    # Verify Code
    api.add_resource(VerifyCodeController, VerifyCodeController.route)

addServiceLayer(api)

if __name__ == '__main__':
    app.run(debug=True)
