from db.mongo_client import Connection
from decouple import config

__dbmanager__ = Connection(config('ROLE_COLLECTION'))

def db_find_active_roles():
    try:
        roles_cursor = __dbmanager__.collection.find({'is_active': True})
        roles_list = list(roles_cursor)
        return roles_list
    except Exception as e:
        raise RuntimeError(f'Error finding active roles: {str(e)}')
    
def db_find_default_role():
    try:
        default_role = __dbmanager__.collection.find_one({'default_role': True})
        return default_role
    except Exception as e:
        raise RuntimeError(f'Error finding default role: {str(e)}')