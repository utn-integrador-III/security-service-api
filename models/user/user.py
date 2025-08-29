import logging
from bson import ObjectId
from utils.encryption_utils import EncryptionUtil
from models.user.db_queries import __dbmanager__, update_token as _unused_update_token, update_password as _unused_update_password

class UserModel:

    def __init__(self, name, password, email, apps):
        self.name = name
        self.password = password
        self.email = email
        self.apps = apps
    
    def to_dict(self):
        # Solo los campos permitidos en root
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'apps': self.apps
        }
    
    @classmethod
    def create_user(cls, user_data):
        try:
            # Encriptar password
            encryption_util = EncryptionUtil()
            user_data['password'] = encryption_util.encrypt(user_data['password'])

            # Asegurar que no vengan campos prohibidos en root
            user_data.pop('status', None)
            user_data.pop('is_session_active', None)

            # Insertar en BD
            result = __dbmanager__.create_data(user_data)
            if result:
                return cls(
                    name=user_data['name'],
                    password=user_data['password'],
                    email=user_data['email'],
                    apps=user_data['apps']
                )
            else:
                raise Exception("Failed to create user in database")
        except Exception as e:
            logging.error(f"Error creating user: {str(e)}", exc_info=True)
            raise Exception('Error creating user')

    @staticmethod
    def find_by_email(email):
        try:
            user = __dbmanager__.find_by_email(email)
            if user:
                user['id'] = str(user.pop('_id'))
            return user
        except Exception as e:
            raise Exception(f"Error in find_by_email: {str(e)}")
        
    @staticmethod
    def logout_user(email):
        """Cierra sesión en TODAS las apps del usuario (apps[].is_session_active = False)."""
        try:
            # Intento con operador $[] (si tu db_manager lo soporta)
            res = __dbmanager__.update_by_condition({'email': email}, {'apps.$[].is_session_active': False})
            if res is None or getattr(res, "matched_count", 0) == 0:
                # Fallback manual
                doc = __dbmanager__.find_by_email(email)
                if not doc:
                    return False
                apps = doc.get('apps', []) or []
                for a in apps:
                    a['is_session_active'] = False
                __dbmanager__.update_by_condition({'email': email}, {'apps': apps})
            return True
        except Exception as e:
            raise Exception(f"Error logging out user: {str(e)}")

    @staticmethod
    def verify_password(plain_password, encrypted_password):
        encryption_util = EncryptionUtil()
        return encryption_util.verify_password(plain_password, encrypted_password)

    @classmethod
    def update_password(cls, email, new_password):
        try:
            result = __dbmanager__.update_by_condition(
                {"email": email},
                {"password": new_password}
            )
            if not result:
                raise Exception("Failed to update password in the database")
        except Exception as e:
            logging.error(f"Error updating password: {str(e)}", exc_info=True)
            raise Exception('Error updating password')
        
    @staticmethod
    def update_reset_password_info(user_email, verification_code, expiration_time, encrypted_temp_password):
        """Para reset: solo actualizamos password. (No tocar status en root)."""
        try:
            update_data = {
                'password': encrypted_temp_password
                # Si quisieras marcar algo por app, hazlo en controllers sobre apps[].
            }
            result = __dbmanager__.update_by_condition({'email': user_email}, update_data)
            if result is None or result.matched_count == 0:
                logging.warning(f"Failed to update reset password info for user: {user_email}. User not found or no changes made.")
                return False
            else:
                logging.info(f"Successfully updated reset password info for user: {user_email}")
                return True
        except Exception as e:
            logging.error(f"Error updating reset password info: {str(e)}", exc_info=True)
            raise Exception('Error updating reset password info')

    @staticmethod
    def update_token(user_id, token):
        """
        Antes se guardaba token en root. Ahora lo aplicamos a TODAS las apps del usuario
        (apps.$[].token = token, apps.$[].is_session_active = True).
        Si quieres token por app, crea otra función con app_id.
        """
        try:
            object_id = ObjectId(user_id)
        except Exception as e:
            logging.error(f"Error converting user_id to ObjectId: {e}")
            return False

        try:
            # Intento con operador $[]
            result = __dbmanager__.update_by_condition(
                {'_id': object_id},
                {'apps.$[].token': token, 'apps.$[].is_session_active': True}
            )
            if result is None or getattr(result, "matched_count", 0) == 0:
                # Fallback manual
                user = __dbmanager__.get_by_id(str(object_id))
                if not user:
                    logging.error("Token update failed: user not found.")
                    return False
                apps = user.get('apps', []) or []
                for a in apps:
                    a['token'] = token
                    a['is_session_active'] = True
                __dbmanager__.update_by_condition({'_id': object_id}, {'apps': apps})
            return True
        except Exception as e:
            logging.error(f"Error updating token: {e}", exc_info=True)
            return False

    @staticmethod
    def user_activation(email):
        """
        Compatibilidad con código viejo: activa TODAS las apps del usuario y
        asegura is_session_active = False a nivel app. (No escribe status en root).
        """
        try:
            # Intento con operador $[]
            res = __dbmanager__.update_by_condition(
                {'email': email},
                {'apps.$[].status': 'active', 'apps.$[].is_session_active': False}
            )
            if res is None or getattr(res, "matched_count", 0) == 0:
                # Fallback manual
                doc = __dbmanager__.find_by_email(email)
                if not doc:
                    return False
                apps = doc.get('apps', []) or []
                for a in apps:
                    a['status'] = 'active'
                    a['is_session_active'] = False
                __dbmanager__.update_by_condition({'email': email}, {'apps': apps})
            return True
        except Exception as e:
            logging.error(f"Error saving user to database: {str(e)}", exc_info=True)
            raise Exception('Error saving user to database')
        
    @staticmethod
    def update_user(email, update_data):

        update_data.pop('status', None)
        update_data.pop('is_session_active', None)

        try:
            result = __dbmanager__.update_by_condition({'email': email}, update_data)
            if result is None or result.matched_count == 0:
                logging.warning(f"Failed to update user: {email}. User not found or no changes made.")
                return False
            else:
                logging.info(f"Successfully updated user: {email}")
                return True
        except Exception as e:
            logging.error(f"Error updating user: {str(e)}", exc_info=True)
            raise Exception('Error updating user')
