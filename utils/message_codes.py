"""
This file defines the message codes for multilanguage in the frontend
Using i18n standard, please check multilanguage folder to add or modify messages
assets/i18n/<lang>
"""
# Authentication Messages
INVALID_EMAIL_DOMAIN = 'INVALID_EMAIL_DOMAIN'
INVALID_CREDENTIALS = 'INVALID_CREDENTIALS'
DECRYPTION_ERROR = 'DECRYPTION_ERROR'
USER_NOT_ACTIVE = 'USER_NOT_ACTIVE'
USER_AUTHENTICATED = 'USER_AUTHENTICATED'
USER_ALREADY_REGISTERED_GENERATING_NEW_CODE = "USER_ALREADY_REGISTERED_GENERATING_NEW_CODE"
USER_ALREADY_REGISTERED = "USER_ALREADY_REGISTERED"
USER_SUCCESSFULLY_CREATED = "USER_SUCCESSFULLY_CREATED"
INVALID_NAME = "INVALID_NAME"
INVALID_PASSWORD = "INVALID_PASSWORD"
USER_SUCCESSFULLY_ENROLLED = "USER_SUCCESSFULLY_ENROLLED"
USER_ALREADY_ENROLLED = "USER_ALREADY_ENROLLED"

# Common Messages
OK_MSG = 'OK_MSG'
CREATED_MSG = 'CREATED_MSG'
NOT_FOUND_MSG = 'NOT_FOUND_MSG'
CONFLICT_MSG = 'CONFLICT_MSG'
UNPROCESSABLE_ENTITY_MSG = 'UNPROCESSABLE_ENTITY_MSG'
INTERNAL_SERVER_ERROR_MSG = 'INTERNAL_SERVER_ERROR_MSG'
SERVER_TIMEOUT_MSG = 'SERVER_TIMEOUT_MSG'
NO_DATA = 'NO_DATA'

# Common Validations Messages
INVALID_ID = 'INVALID_ID' # Invalid Id

# Health Validations Messages
HEALTH_NOT_FOUND = 'HEALTH_NOT_FOUND' # Health not found
HEALTH_SUCCESSFULLY = "HEALTH_SUCCESSFULLY" # Health successfully responded

# USER Validations Messages
USER_NOT_FOUND = 'USER_NOT_FOUND' # User not found
USER_SUCCESSFULLY_UPDATED = "USER_SUCCESSFULLY_UPDATED" # User successfully updated
USER_SUCCESSFULLY_DELETED = "USER_SUCCESSFULLY_DELETED" # User successfully deleted
USER_DELETE_HAS_RELATIONS = "USER_DELETE_HAS_RELATIONS" # User cannot be deleted
USER_ALREDY_REGISTERED = "USER_ALREDY_REGISTERED" # User already registered
USER_CODE_VERIFICATIN_VALIDATED = "USER_CODE_VERIFICATIN_VALIDATED" # Code verification is validated
INVALID_EMAIL_DOMAIN = 'INVALID_EMAIL_DOMAIN' #The domian is incorrect
INVALID_NAME = 'INVALID_NAME'  # Invalid name
INVALID_PASSWORD = 'INVALID_PASSWORD'  # Invalid password
USER_ALREDY_REGISTERED_GENERATING_NEW_CODE = "USER_ALREDY_REGISTERED_GENERATING_NEW_CODE"

# ROL Validations Messages
ROL_FOUND="ROL_FOUND"
ROL_NOT_FOUND = 'ROL_NOT_FOUND' # Rol not found
ROL_SUCCESSFULLY_UPDATED = "ROL_SUCCESSFULLY_UPDATED" # Rol successfully updated
ROL_SUCCESSFULLY_DELETED = "ROL_SUCCESSFULLY_DELETED" # Rol successfully deleted
ROL_SUCCESSFULLY_CREATED = "ROL_SUCCESSFULLY_CREATED" # Rol created successfully
ROL_ALREADY_REGISTERED = "ROL_ALREADY_REGISTERED"
ROL_SUCCESSFULLY_ENROLLED = "ROL_SUCCESSFULLY_ENROLLED"
INVALID_ROLE = "INVALID_ROLE"

#Password Validations Messages
MISSING_REQUIRED_FIELDS = "MISSING_REQUIRED_FIELDS"
USER_NOT_FOUND = "USER_NOT_FOUND"
USER_NOT_ACTIVE = "USER_NOT_ACTIVE"
INVALID_OLD_PASSWORD = "INVALID_OLD_PASSWORD"
PASSWORDS_DO_NOT_MATCH = "PASSWORDS_DO_NOT_MATCH"
PASSWORD_UPDATED_SUCCESSFULLY = "PASSWORD_UPDATED_SUCCESSFULLY"
UNEXPECTED_ERROR_OCCURRED = "UNEXPECTED_ERROR_OCCURRED"
PASSWORD_RESET_INITIATED = "PASSWORD_RESET_INITIATED"
UPDATE_USER_FAILED = "UPDATE_USER_FAILED"

USER_CODE_VERIFICATION_VALIDATED = "USER_CODE_VERIFICATION_VALIDATED" # Code verification is validated
INVALID_ROLE = "INVALID_ROLE"
NO_ACTIVE_ROLES_FOUND = "NO_ACTIVE_ROLES_FOUND"
DEFAULT_ROLE_NOT_FOUND = "DEFAULT_ROLE_NOT_FOUND"
USER_CREATION_ERROR = "USER_CREATION_ERROR"
UNEXPECTED_ERROR = "UNEXPECTED_ERROR"
CREATED = "CREATED"

# Mensajes de verificación de código
INVALID_VERIFICATION_CODE = "INVALID_VERIFICATION_CODE"
VERIFICATION_SUCCESSFUL = "VERIFICATION_SUCCESSFUL"
VERIFICATION_EXPIRED = "VERIFICATION_EXPIRED"