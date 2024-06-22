from flask_restful import Resource
from controllers.health.controller import HealthController
from controllers.user.user_controller import UserController
from flask_restful import Api

def addServiceLayer(api: Api):
   
    api.add_resource(HealthController, HealthController.route)
    api.add_resource(UserController, '/register')
    
   
    
    