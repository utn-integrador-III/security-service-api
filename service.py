from flask_restful import Resource
from controllers.health.controller import HealthController
from flask_restful import Api

def addServiceLayer(api: Api):
   
    api.add_resource(HealthController, HealthController.route)
    
   
    
    