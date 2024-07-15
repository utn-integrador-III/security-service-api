from flask_restful import Api
from controllers.health.controller import HealthController
from controllers.auth.auth import AuthController
from controllers.user.UserEnrollment_controller import UserEnrollmentController

def addServiceLayer(api: Api):
    # Health
    api.add_resource(HealthController, HealthController.route)
    
    # Auth
    api.add_resource(AuthController, AuthController.route)
    
    # User
    api.add_resource(UserEnrollmentController, UserEnrollmentController.route)
