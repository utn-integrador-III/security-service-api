from flask_restful import Api
from controllers.user.UserPasswordController import UserPasswordController
from controllers.auth.logout import LogoutController
from controllers.health.controller import HealthController
from controllers.auth.auth import LoginController
from controllers.auth.verify_auth import AuthController
from controllers.rol.rol_controller import RolController
from controllers.user.UserEnrollment_controller import UserEnrollmentController
def addServiceLayer(api: Api):
    # Health
    api.add_resource(HealthController, HealthController.route)
    
    # Auth
    api.add_resource(AuthController, AuthController.route)
    api.add_resource(LoginController, LoginController.route)
    # Rol
    api.add_resource(RolController, RolController.route)

    #Logout
    api.add_resource(LogoutController,LogoutController.route)
    # User
    api.add_resource(UserEnrollmentController, UserEnrollmentController.route)
    api.add_resource(UserPasswordController, UserPasswordController.route)




