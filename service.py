from flask_restful import Api
from controllers.auth.logout import LogoutController
from controllers.health.controller import HealthController
from controllers.auth.auth import AuthController
from controllers.user.UserEnrollment_controller import UserEnrollmentController

def addServiceLayer(api: Api):
    # Health
    api.add_resource(HealthController, HealthController.route)
    
    # Auth
    api.add_resource(AuthController, AuthController.route)

    #Logout
    api.add_resource(LogoutController,LogoutController.route)
    
    # User
    api.add_resource(UserEnrollmentController, UserEnrollmentController.route)
