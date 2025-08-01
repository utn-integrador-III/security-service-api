from flask_restful import Api
from controllers.user.UserPasswordController import UserPasswordController
from controllers.auth.logout import LogoutController
from controllers.health.controller import HealthController
from controllers.auth.auth import LoginController
from controllers.auth.verify_auth import AuthController
from controllers.auth.refresh_token import RefreshController
from controllers.rol.rol_controller import RolController
from controllers.user.UserVerificationController import UserVerificationController
from controllers.user.UserActivationController import UserActivationController
from controllers.user.UserAppController import UserAppController
from controllers.user.UserEnrollment_controller import UserEnrollmentController
def addServiceLayer(api: Api):
    # Health
    api.add_resource(HealthController, HealthController.route)
    
    # Auth
    api.add_resource(AuthController, AuthController.route)
    api.add_resource(LoginController, LoginController.route)
    api.add_resource(RefreshController, RefreshController.route)
    # Rol
    api.add_resource(RolController, RolController.route)

    #Logout
    api.add_resource(LogoutController,LogoutController.route)
    # User
    api.add_resource(UserEnrollmentController, UserEnrollmentController.route)
    api.add_resource(UserPasswordController, UserPasswordController.route)
    
    api.add_resource(UserVerificationController, UserVerificationController.route)
    api.add_resource(UserActivationController, UserActivationController.route)
    api.add_resource(UserAppController, UserAppController.route)
