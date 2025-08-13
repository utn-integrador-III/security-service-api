# controllers/user/user_controller.py
import logging
import random
from datetime import datetime, timedelta
from bson import ObjectId
from flask import request, make_response
from flask_restful import Resource
from validate_email import validate_email

from models.user.user import UserModel
from models.role.role import RoleModel
from models.user.db_queries import __dbmanager__
from models.apps.db_queries import get_by_name as get_app_by_name

from utils.email_manager import send_email, send_email_new_password
from utils.server_response import ServerResponse, StatusCode
from utils.auth_manager import generate_verification_code
from utils.encryption_utils import EncryptionUtil
from utils.password_validator import validate_password

from utils.message_codes import (
    CREATED, INVALID_EMAIL_DOMAIN, INVALID_NAME, INVALID_PASSWORD,
    USER_ALREADY_REGISTERED, USER_CREATION_ERROR, UNEXPECTED_ERROR,
    MISSING_REQUIRED_FIELDS, USER_NOT_FOUND, USER_NOT_ACTIVE,
    INVALID_OLD_PASSWORD, PASSWORDS_DO_NOT_MATCH, PASSWORD_UPDATED_SUCCESSFULLY,
    UNEXPECTED_ERROR_OCCURRED, PASSWORD_RESET_INITIATED, UPDATE_USER_FAILED,
    INVALID_VERIFICATION_CODE, VERIFICATION_EXPIRED, VERIFICATION_SUCCESSFUL
)

# =========================================
# POST /user/enrollment
# =========================================
class UserEnrollmentController(Resource):
    route = '/user/enrollment'

    def post(self):
        try:
            data = request.get_json(force=True, silent=True) or {}

            name = data.get('name')
            email = data.get('email')
            password = data.get('password')

            # modo simple
            role_name = data.get('role_name')
            app_name  = data.get('app_name')

            # modo arreglo (compatibilidad)
            apps_body = data.get('apps', [])

            # -------- Validaciones base --------
            if not name or len(name.strip()) < 2:
                return ServerResponse(
                    message="The name does not meet the established standards",
                    message_code=INVALID_NAME,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            if not email or not validate_email(email):
                return ServerResponse(
                    message="The provided email is not valid",
                    message_code=INVALID_EMAIL_DOMAIN,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            if not password or len(password) < 8:
                return ServerResponse(
                    message="The password does not meet the established standards",
                    message_code=INVALID_PASSWORD,
                    status=StatusCode.UNPROCESSABLE_ENTITY
                ).to_response()

            policy_msg = validate_password(password)
            if policy_msg:
                return ServerResponse(message=policy_msg, status=StatusCode.BAD_REQUEST).to_response()

            # -------- Construcción de apps_to_assign --------
            apps_to_assign = []

            # 1) role_name + app_name
            if role_name or app_name:
                if not role_name or not app_name:
                    return ServerResponse(
                        message="Both 'role_name' and 'app_name' are required",
                        status=StatusCode.BAD_REQUEST
                    ).to_response()

                role_doc = RoleModel.get_by_name(role_name)
                if not role_doc or not role_doc.get("_id"):
                    return ServerResponse(
                        message=f"Invalid role: {role_name}",
                        status=StatusCode.UNPROCESSABLE_ENTITY
                    ).to_response()
                role_oid = ObjectId(str(role_doc["_id"]))

                app_doc = get_app_by_name(app_name)
                if not app_doc or not app_doc.get("_id"):
                    return ServerResponse(
                        message=f"Application not found: {app_name}",
                        status=StatusCode.NOT_FOUND
                    ).to_response()
                app_oid = ObjectId(str(app_doc["_id"]))

                apps_to_assign.append({
                    "role": role_oid,
                    "app":  app_oid,
                    "code": str(random.randint(100000, 999999)),
                    "token": "",
                    "status": "Pending",
                    "code_expliration": (datetime.utcnow() + timedelta(minutes=5)).strftime("%Y/%m/%d %H:%M:%S"),
                    "is_session_active": False
                })

            # 2) arreglo apps[] 
            for ap in apps_body or []:
                role_val = ap.get("role")
                app_val  = ap.get("app")
                if not role_val or not app_val:
                    return ServerResponse(
                        message="Each app item must include 'role' and 'app'",
                        status=StatusCode.UNPROCESSABLE_ENTITY
                    ).to_response()

                try:
                    role_oid = ObjectId(role_val)
                except Exception:
                    rdoc = RoleModel.get_by_name(role_val)
                    if not rdoc or not rdoc.get("_id"):
                        return ServerResponse(
                            message=f"Invalid role: {role_val}",
                            status=StatusCode.UNPROCESSABLE_ENTITY
                        ).to_response()
                    role_oid = ObjectId(str(rdoc["_id"]))

                try:
                    app_oid = ObjectId(app_val)
                except Exception:
                    adoc = get_app_by_name(app_val)
                    if not adoc or not adoc.get("_id"):
                        return ServerResponse(
                            message=f"Application not found: {app_val}",
                            status=StatusCode.NOT_FOUND
                        ).to_response()
                    app_oid = ObjectId(str(adoc["_id"]))

                apps_to_assign.append({
                    "role": role_oid,
                    "app":  app_oid,
                    "code": str(random.randint(100000, 999999)),
                    "token": "",
                    "status": "Pending",
                    "code_expliration": (datetime.utcnow() + timedelta(minutes=5)).strftime("%Y/%m/%d %H:%M:%S"),
                    "is_session_active": False
                })

            if not apps_to_assign:
                return ServerResponse(
                    message="At least one role/app assignment is required.",
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            # -------- Lógica principal  --------
            existing_user = UserModel.find_by_email(email)
            if existing_user:
                user_apps = existing_user.get("apps", []) or []

                for new_app in apps_to_assign:
                    dup = any(
                        str(ua.get("role")) == str(new_app["role"]) and
                        str(ua.get("app"))  == str(new_app["app"])
                        for ua in user_apps
                    )
                    if dup:
                        return ServerResponse(
                            message=f"User already assigned to role '{new_app['role']}' and app '{new_app['app']}'.",
                            message_code=USER_ALREADY_REGISTERED,
                            status=StatusCode.CONFLICT
                        ).to_response()

                user_apps.extend(apps_to_assign)
                
                UserModel.update_user(email, {"apps": user_apps})

                for ap in apps_to_assign:
                    try:
                        send_email(email, ap["code"])
                    except Exception as e:
                        logging.warning(f"Email send failed to {email}: {e}")

                return ServerResponse(
                    message="User updated with new role(s) and app(s). Verification code(s) sent.",
                    message_code=CREATED,
                    status=StatusCode.OK
                ).to_response()

            # crear usuario 
            user_data = {
                "name": name.strip(),
                "password": password,
                "email": email.strip(),
                "apps": apps_to_assign
            }
            UserModel.create_user(user_data)

            for ap in apps_to_assign:
                try:
                    send_email(email, ap["code"])
                except Exception as e:
                    logging.warning(f"Email send failed to {email}: {e}")

            return ServerResponse(
                message="User created successfully and verification code(s) sent.",
                message_code=CREATED,
                status=StatusCode.CREATED
            ).to_response()

        except Exception as e:
            logging.error(f"[POST /user/enrollment] {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                message_code=UNEXPECTED_ERROR,
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()


# =========================================
# GET /user?app_id=
# =========================================
class UsersListController(Resource):
    route = '/user'

    def get(self):
        try:
            app_id = request.args.get('app_id')
            query = {}

            if app_id:
                try:
                    app_oid = ObjectId(app_id)
                except Exception:
                    adoc = get_app_by_name(app_id)
                    if not adoc or not adoc.get("_id"):
                        return ServerResponse(
                            message="Application not found",
                            status=StatusCode.NOT_FOUND
                        ).to_response()
                    app_oid = ObjectId(str(adoc["_id"]))

                query = {"apps": {"$elemMatch": {"app": app_oid}}}

            cursor = __dbmanager__.get_by_query(query)
            data = []
            for d in cursor or []:
                d = dict(d)
                d["id"] = str(d.pop("_id"))
                data.append(d)

            return ServerResponse(data=data, status=StatusCode.OK).to_response()

        except Exception as e:
            logging.error(f"[GET /user] {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                message_code=UNEXPECTED_ERROR,
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()


# =========================================
# GET|PATCH|DELETE /user/<id>
# =========================================
class UserItemController(Resource):
    route = '/user/<string:id>'

    def get(self, id: str):
        try:
            doc = __dbmanager__.get_by_id(id)
            if not doc or isinstance(doc, Exception):
                return ServerResponse(
                    message="User not found",
                    message_code=USER_NOT_FOUND,
                    status=StatusCode.NOT_FOUND
                ).to_response()
            d = dict(doc)
            d["id"] = str(d.pop("_id"))
            return ServerResponse(data=d, status=StatusCode.OK).to_response()
        except Exception as e:
            logging.error(f"[GET /user/{id}] {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                message_code=UNEXPECTED_ERROR,
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()

    def patch(self, id: str):
        """
        Cambios dentro de apps[] (siempre requiere app_id):
        - {"app_id":"<id|name>", "is_session_active": true|false}
        - {"app_id":"<id|name>", "status":"Active|Pending|inactive"}
        - {"app_id":"<id|name>", "role":"<roleId|roleName>"}
        """
        try:
            data = request.get_json(force=True, silent=True) or {}

            app_in = data.get("app_id")
            if not app_in:
                return ServerResponse(
                    message="Field 'app_id' is required to update app fields (status, role, is_session_active).",
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            try:
                app_oid = ObjectId(app_in)
            except Exception:
                adoc = get_app_by_name(app_in)
                if not adoc or not adoc.get("_id"):
                    return ServerResponse(
                        message="Application not found",
                        status=StatusCode.NOT_FOUND
                    ).to_response()
                app_oid = ObjectId(str(adoc["_id"]))

            updates = {}
            if "status" in data:
                updates["apps.$.status"] = data["status"]
            if "role" in data and data["role"]:
                val = data["role"]
                try:
                    role_oid = ObjectId(val)
                except Exception:
                    rdoc = RoleModel.get_by_name(val)
                    if not rdoc or not rdoc.get("_id"):
                        return ServerResponse(
                            message="Invalid role",
                            status=StatusCode.UNPROCESSABLE_ENTITY
                        ).to_response()
                    role_oid = ObjectId(str(rdoc["_id"]))
                updates["apps.$.role"] = role_oid
            if "is_session_active" in data:
                updates["apps.$.is_session_active"] = bool(data["is_session_active"])

            if not updates:
                return ServerResponse(message="No changes provided", status=StatusCode.BAD_REQUEST).to_response()

            result = __dbmanager__.update_by_condition(
                {"_id": ObjectId(id), "apps.app": app_oid},
                updates
            )
            if result is None or getattr(result, "matched_count", 0) == 0:
                return ServerResponse(message="User or app assignment not found", status=StatusCode.NOT_FOUND).to_response()

            doc = __dbmanager__.get_by_id(id)
            d = dict(doc); d["id"] = str(d.pop("_id"))
            return ServerResponse(message="User app updated", data=d, status=StatusCode.OK).to_response()

        except Exception as e:
            logging.error(f"[PATCH /user/{id}] {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                message_code=UNEXPECTED_ERROR,
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()

    def delete(self, id: str):
        """
        Inactiva todos los accesos del usuario (apps[]):
        - apps.$[].status = 'inactive'
        - apps.$[].is_session_active = False
        """
        try:
            result = __dbmanager__.update_by_condition(
                {"_id": ObjectId(id)},
                {"apps.$[].status": "inactive", "apps.$[].is_session_active": False}
            )
            if result is None or getattr(result, "matched_count", 0) == 0:
                # Fallback manual
                doc = __dbmanager__.get_by_id(id)
                if not doc or isinstance(doc, Exception):
                    return ServerResponse(message="User not found", message_code=USER_NOT_FOUND, status=StatusCode.NOT_FOUND).to_response()
                d = dict(doc)
                apps = d.get("apps", []) or []
                for a in apps:
                    a["status"] = "inactive"
                    a["is_session_active"] = False
                __dbmanager__.update_by_condition({"_id": ObjectId(id)}, {"apps": apps})

            updated = __dbmanager__.get_by_id(id)
            d = dict(updated); d["id"] = str(d.pop("_id"))
            return ServerResponse(message="All accesses inactivated", data=d, status=StatusCode.OK).to_response()

        except Exception as e:
            logging.error(f"[DELETE /user/{id}] {str(e)}", exc_info=True)
            return ServerResponse(
                message="An unexpected error occurred.",
                message_code=UNEXPECTED_ERROR,
                status=StatusCode.INTERNAL_SERVER_ERROR
            ).to_response()


# =========================================
#  /user/password  (PUT | POST)
# =========================================
class UserPasswordController(Resource):
    route = '/user/password'

    def put(self):
        try:
            data = request.json or {}
            user_email = data.get('user_email')
            old_password = data.get('old_password')
            new_password = data.get('new_password')
            confirm_password = data.get('confirm_password')

            if not all([user_email, old_password, new_password, confirm_password]):
                return ServerResponse(
                    message="All fields are required: user_email, old_password, new_password, confirm_password",
                    message_code=MISSING_REQUIRED_FIELDS,
                    status=StatusCode.BAD_REQUEST
                ).to_response()

            user = UserModel.find_by_email(user_email)
            if not user:
                return ServerResponse(message="User not found", message_code=USER_NOT_FOUND, status=StatusCode.NOT_FOUND).to_response()

            # validar que tenga al menos una app activa
            if not any((a.get('status') == 'Active') for a in (user.get('apps') or [])):
                return ServerResponse(message="User is not active", message_code=USER_NOT_ACTIVE, status=StatusCode.FORBIDDEN).to_response()

            if not UserModel.verify_password(old_password, user['password']):
                return ServerResponse(message="Old password is incorrect", message_code=INVALID_OLD_PASSWORD, status=StatusCode.UNAUTHORIZED).to_response()

            msg = validate_password(new_password)
            if msg:
                return ServerResponse(message=msg, status=StatusCode.BAD_REQUEST).to_response()

            if new_password != confirm_password:
                return ServerResponse(message="New password and confirm password do not match", message_code=PASSWORDS_DO_NOT_MATCH, status=StatusCode.BAD_REQUEST).to_response()

            encrypted_password = EncryptionUtil().encrypt(new_password)
            UserModel.update_password(user_email, encrypted_password)

            return ServerResponse(message="Password updated successfully", message_code=PASSWORD_UPDATED_SUCCESSFULLY, status=StatusCode.OK).to_response()

        except Exception as e:
            logging.error(f"[PUT /user/password] {str(e)}", exc_info=True)
            return ServerResponse(message="An unexpected error occurred.", message_code=UNEXPECTED_ERROR_OCCURRED, status=StatusCode.INTERNAL_SERVER_ERROR).to_response()

    def post(self):
        try:
            data = request.json or {}
            user_email = data.get('email')
            if not user_email:
                return ServerResponse(message="User email is required", message_code=MISSING_REQUIRED_FIELDS, status=StatusCode.BAD_REQUEST).to_response()

            user = UserModel.find_by_email(user_email)
            if not user:
                return ServerResponse(message="User not found", message_code=USER_NOT_FOUND, status=StatusCode.NOT_FOUND).to_response()

            verification_code = generate_verification_code()
            expiration_time = datetime.utcnow() + timedelta(minutes=5)
            email_prefix = user_email.split('@')[0]
            temporal_password = f"{email_prefix}{verification_code}"

            encrypted_temp_password = EncryptionUtil().encrypt(temporal_password)
            updated = UserModel.update_reset_password_info(user_email, verification_code, expiration_time, encrypted_temp_password)

            if updated:
                try:
                    send_email_new_password(user_email, temporal_password)
                except Exception as e:
                    logging.warning(f"Failed to send temp password to {user_email}: {e}")
                return ServerResponse(message="Password reset initiated", message_code=PASSWORD_RESET_INITIATED, status=StatusCode.OK).to_response()

            return ServerResponse(message="Failed to update user information", message_code=UPDATE_USER_FAILED, status=StatusCode.INTERNAL_SERVER_ERROR).to_response()

        except Exception as e:
            logging.error(f"[POST /user/password] {str(e)}", exc_info=True)
            return ServerResponse(message="An unexpected error occurred.", message_code=UNEXPECTED_ERROR_OCCURRED, status=StatusCode.INTERNAL_SERVER_ERROR).to_response()


# =========================================
#  /user/verification  (PUT)  -> valida en apps[].code
# =========================================
class UserVerificationController(Resource):
    route = '/user/verification'

    def options(self):
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response

    def put(self):
        try:
            data = request.json or {}
            email = data.get('user_email')
            code = str(data.get('verification_code') or "")

            user = UserModel.find_by_email(email)
            if not user:
                return ServerResponse(message="User not found", message_code=USER_NOT_FOUND, status=StatusCode.NOT_FOUND).to_response()

            apps = user.get('apps') or []
            # localizar la app por código
            target = next((a for a in apps if str(a.get('code')) == code), None)
            if not target:
                return ServerResponse(message="Invalid verification code", message_code=INVALID_VERIFICATION_CODE, status=StatusCode.UNAUTHORIZED).to_response()

            # validar expiración (YYYY/MM/DD HH:mm:SS)
            exp_str = target.get('code_expliration')
            try:
                exp_dt = datetime.strptime(exp_str, "%Y/%m/%d %H:%M:%S") if exp_str else None
            except Exception:
                exp_dt = None
            if exp_dt and exp_dt < datetime.utcnow():
                return ServerResponse(message="Verification code expired", message_code=VERIFICATION_EXPIRED, status=StatusCode.UNAUTHORIZED).to_response()

            # activar SOLO esa app y limpiar el código
            target['status'] = 'Active'
            target['code'] = ''
            target['code_expliration'] = ''

            # guardar cambios (sin tocar status en root)
            UserModel.update_user(email, {"apps": apps})

            return ServerResponse(message="User successfully verified", message_code=VERIFICATION_SUCCESSFUL, status=StatusCode.OK).to_response()

        except Exception as e:
            logging.error(f"[PUT /user/verification] {str(e)}", exc_info=True)
            return ServerResponse(message="An unexpected error occurred.", status=StatusCode.INTERNAL_SERVER_ERROR).to_response()
