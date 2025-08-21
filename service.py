from flask_restful import Api
from controllers.auth.logout import LogoutController
from controllers.health.controller import HealthController
from controllers.auth.auth import LoginController
from controllers.auth.admin_login import AdminLoginController
from controllers.auth.verify_auth import AuthController
from controllers.auth.refresh_token import RefreshController
from controllers.rol.rol_controller import RolController
from controllers.rol.rol_item_controller import RolItemController
from controllers.admin.admin_controller import AdminListController, AdminItemController
from controllers.apps.apps_controller import AppsListController, AppsItemController
from controllers.user.user_controller import (
    UserEnrollmentController,
    UsersListController,
    UserItemController,
    UserPasswordController,
    UserVerificationController
)
def addServiceLayer(api: Api):
    # Health
    api.add_resource(HealthController, HealthController.route)
    
    # Auth
    api.add_resource(AuthController, AuthController.route)
    api.add_resource(LoginController, LoginController.route)
    api.add_resource(AdminLoginController, AdminLoginController.route)
    api.add_resource(RefreshController, RefreshController.route)
    # Rol
    api.add_resource(RolController, RolController.route)
    api.add_resource(RolItemController, RolItemController.route)

    #Logout
    api.add_resource(LogoutController,LogoutController.route)
    # User
    api.add_resource(UserEnrollmentController, UserEnrollmentController.route)
    api.add_resource(UserPasswordController, UserPasswordController.route)
    api.add_resource(UsersListController, UsersListController.route)
    api.add_resource(UserVerificationController, UserVerificationController.route)
    api.add_resource(UserItemController,  UserItemController.route)

    # User_Admin
    api.add_resource(AdminListController, AdminListController.route)
    api.add_resource(AdminItemController, AdminItemController.route)

    # Apps
    api.add_resource(AppsListController, AppsListController.route)
    api.add_resource(AppsItemController, AppsItemController.route)
