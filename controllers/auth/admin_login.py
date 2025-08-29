# controllers/admin_login_controller.py
from flask_restful import Resource, reqparse
from utils.server_response import StatusCode, ServerResponse
from utils.jwt_manager import generate_jwt
from utils.email_validator import is_valid_email_domain
import bcrypt
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno para conexión directa a MongoDB
load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client['security']
admin_collection = db['user_admin']

class AdminLoginController(Resource):
    route = '/auth/admin/login'

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', required=True, help="Email cannot be blank!")
        self.parser.add_argument('password', required=True, help="Password cannot be blank!")

    def post(self):
        args = self.parser.parse_args()
        email = args['email']
        password = args['password']

        if not is_valid_email_domain(email):
            return ServerResponse(
                message="Invalid email domain",
                message_code="INVALID_EMAIL_DOMAIN",
                status=StatusCode.BAD_REQUEST
            ).to_response()

        # Buscar en la colección de user_admin
        admin = admin_collection.find_one({"admin_email": email})
        
        if not admin:
            return ServerResponse(
                message="Invalid email or password",
                message_code="INVALID_CREDENTIALS",
                status=StatusCode.UNAUTHORIZED
            ).to_response()

        # Verificar contraseña (bcrypt)
        password_valid = False
        try:
            password_valid = bcrypt.checkpw(password.encode('utf-8'), admin['password_secret'].encode('utf-8'))
        except:
            password_valid = False

        if not password_valid:
            return ServerResponse(
                message="Invalid email or password",
                message_code="INVALID_CREDENTIALS",
                status=StatusCode.UNAUTHORIZED
            ).to_response()

        if admin.get('status') != "active":
            return ServerResponse(
                message="Admin is not active",
                message_code="ADMIN_NOT_ACTIVE",
                status=StatusCode.FORBIDDEN
            ).to_response()

        # Generar token JWT para admin
        identity = str(admin['_id'])
        email = admin['admin_email']
        name = f"Admin {admin['admin_email'].split('@')[0]}"
        status = admin.get('status', 'active')
        rolName = 'Admin'

        token = generate_jwt(identity, rolName, email, name, status)

        # Actualizar token en la base de datos
        admin_collection.update_one(
            {'_id': admin['_id']},
            {'$set': {'token': token, 'last_login': datetime.utcnow()}}
        )

        return ServerResponse(
            data={
                'email': email,
                'name': name,
                'status': status,
                'role': {
                    'name': 'Admin',
                    'permissions': ['read', 'write', 'delete', 'admin'],
                    'is_active': True,
                    'screens': ['dashboard', 'users', 'apps', 'roles', 'admin']
                },
                'token': token
            },
            message="Admin has been authenticated",
            message_code="ADMIN_AUTHENTICATED",
            status=StatusCode.OK
        ).to_response()
