# controllers/login_controller.py
from flask_restful import Resource, reqparse
from models.user.user import UserModel
from utils.server_response import StatusCode, ServerResponse
from utils.jwt_manager import generate_jwt
from utils.email_validator import is_valid_email_domain
from models.role.role import RoleModel
import bcrypt
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime

# Cargar variables de entorno para conexión directa a MongoDB
load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client['security']
security_collection = db['user']

class LoginController(Resource):
    route = '/auth/login'

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', required=True, help="Email cannot be blank!")
        self.parser.add_argument('password', required=True, help="Password cannot be blank!")
        self.parser.add_argument('app', required=True, help="App cannot be blank!")

    def post(self):
        args = self.parser.parse_args()
        email = args['email']
        password = args['password']
        requested_app = args['app']

        if not is_valid_email_domain(email):
            return ServerResponse(
                message="Invalid email domain",
                message_code="INVALID_EMAIL_DOMAIN",
                status=StatusCode.BAD_REQUEST
            ).to_response()

        # Primero intentar buscar en la colección de usuarios normales
        user = UserModel.find_by_email(email)
        
        # Si no se encuentra, buscar en la colección de security users
        if not user:
            security_user = security_collection.find_one({"email": email})
            if security_user:
                # Convertir el usuario de security a formato compatible
                user = {
                    'id': str(security_user['_id']),
                    'name': security_user['name'],
                    'email': security_user['email'],
                    'password': security_user['password'],
                    'status': security_user.get('status', 'Active'),
                    'apps': security_user.get('apps', []),
                    'token': security_user.get('token', ''),
                    'is_session_active': security_user.get('is_session_active', False)
                }

        if not user:
            return ServerResponse(
                message="Invalid email or password",
                message_code="INVALID_CREDENTIALS",
                status=StatusCode.UNAUTHORIZED
            ).to_response()

        # Verificar contraseña según el tipo de usuario
        password_valid = False
        if user.get('password', '').startswith('$2b$'):  # Usuario de security (bcrypt)
            try:
                password_valid = bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8'))
            except:
                password_valid = False
        else:  # Usuario normal (encriptación personalizada)
            password_valid = UserModel.verify_password(password, user['password'])

        if not password_valid:
            return ServerResponse(
                message="Invalid email or password",
                message_code="INVALID_CREDENTIALS",
                status=StatusCode.UNAUTHORIZED
            ).to_response()

        if user['status'] != "Active":
            return ServerResponse(
                message="User is not active",
                message_code="USER_NOT_ACTIVE",
                status=StatusCode.FORBIDDEN
            ).to_response()

        # Validar que el usuario pertenezca a la app solicitada
        user_has_access_to_app = False
        user_role = None
        user_app_data = None
        app_id = None

        if user.get('apps') and len(user['apps']) > 0:
            # Usuario de security (tiene apps)
            for app in user['apps']:
                if app.get('app') == requested_app:
                    user_has_access_to_app = True
                    user_role = app.get('role', "vehiculos/solicitante")
                    user_app_data = app
                    # Generar o usar ID de app existente
                    app_id = app.get('app_id', str(uuid.uuid4()))
                    break
        else:
            # Usuario normal - por ahora asumimos que tiene acceso a todas las apps
            # En el futuro se puede implementar validación específica
            user_has_access_to_app = True
            user_role = user.get('role', "vehiculos/solicitante")
            app_id = str(uuid.uuid4())  # Generar ID para usuario normal

        if not user_has_access_to_app:
            return ServerResponse(
                message="User does not have access to the requested app",
                message_code="USER_APP_ACCESS_DENIED",
                status=StatusCode.FORBIDDEN
            ).to_response()

        token = generate_jwt(user['id'], user_role, user['email'], user['name'], user['status'])

        # Update user's token and app_id in the database
        if user.get('password', '').startswith('$2b$'):  # Usuario de security
            # Actualizar la app específica con el app_id
            if user_app_data:
                user_app_data['app_id'] = app_id
                user_app_data['last_login'] = datetime.utcnow().isoformat()
                
                # Actualizar en la base de datos
                security_collection.update_one(
                    {"email": email}, 
                    {
                        "$set": {
                            "token": token, 
                            "is_session_active": True,
                            "current_app_id": app_id,
                            "current_app": requested_app,
                            "last_login": datetime.utcnow().isoformat()
                        },
                        "$set": {"apps": user['apps']}
                    }
                )
            else:
                security_collection.update_one(
                    {"email": email}, 
                    {
                        "$set": {
                            "token": token, 
                            "is_session_active": True,
                            "current_app_id": app_id,
                            "current_app": requested_app,
                            "last_login": datetime.utcnow().isoformat()
                        }
                    }
                )
        else:  # Usuario normal
            success = UserModel.update_token(user['id'], token)
            if not success:
                return ServerResponse(
                    message="Failed to update user token",
                    message_code="TOKEN_UPDATE_FAILED",
                    status=StatusCode.INTERNAL_SERVER_ERROR
                ).to_response()
            
            # También actualizar app_id para usuarios normales
            UserModel.update_user(email, {
                "current_app_id": app_id,
                "current_app": requested_app,
                "last_login": datetime.utcnow().isoformat()
            })
        
        # Obtener información del rol desde la base de datos de roles
        role_object = RoleModel.get_by_name(user_role)
        if role_object:
            filtered_role_data = {
                "name": role_object.name,
                "permissions": role_object.permissions,
                "is_active": role_object.is_active,
                "screens": role_object.screens
            }
        else:
            # Si no existe el rol en la BD de roles, usar información básica
            filtered_role_data = {
                "name": user_role,
                "permissions": ["read", "write"],
                "is_active": True,
                "screens": ["default"]
            }

        response_data = {
            'data': {
                "email": user['email'],
                "name": user['name'],
                "status": user['status'],
                "role": filtered_role_data,
                "token": token,
                "app": requested_app,
                "app_id": app_id
            },
            'message': "User has been authenticated",
            'message_code': "USER_AUTHENTICATED"
        }

        # Agregar apps si el usuario las tiene
        if user.get('apps'):
            response_data['data']['apps'] = user['apps']

        return ServerResponse(
            data=response_data['data'],
            message=response_data['message'],
            message_code=response_data['message_code'],
            status=StatusCode.OK
        ).to_response()