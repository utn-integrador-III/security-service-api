from flask_restful import Api
from controllers.health.controller import HealthController
from controllers.auth.auth import LoginController
from controllers.auth.verify_auth import AuthController
from controllers.rol.rol_controller import RolController
from controllers.user.user_controller import UserController

def addServiceLayer(api: Api):
    # Health
    api.add_resource(HealthController, HealthController.route)
    
    # Auth
    api.add_resource(AuthController, AuthController.route)
    api.add_resource(LoginController, LoginController.route)
    # Rol
    api.add_resource(RolController, RolController.route)
    # User
    api.add_resource(UserController, UserController.route)
