from flask import Flask
from swagger_ui import flask_api_doc
from flask_restful import Api
from flask_cors import CORS
from decouple import config
from service import addServiceLayer
import logging

app = Flask(__name__)
app.debug = config('FLASK_DEBUG', cast=bool, default=True)
api = Api(app)
flask_api_doc(app, config_path='./swagger.yml', url_prefix='/api/doc', title='API doc')
logging.basicConfig(level=logging.INFO)

# Configuración CORS mejorada para desarrollo
cors = CORS(app, 
    resources={r"/*": {"origins": "*"}},
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    supports_credentials=True
)

addServiceLayer(api)

if __name__ == "__main__":
    app.run(host=config('FLASK_RUN_HOST', default='0.0.0.0'), 
            port=config('SECURITY_SERVICE_PORT', cast=int, default=5002))