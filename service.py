from flask_restful import Resource
from controllers.health.controller import HealthController
from controllers.auth.auth import AuthController


from flask_restful import Api

def addServiceLayer(api: Api):
    # Health
    api.add_resource(HealthController, HealthController.route)
    
    # User
    # api.add_resource(User, User.route)
    # api.add_resource(UserById, UserById.route)


    api.add_resource(AuthController, AuthController.route)
    
    