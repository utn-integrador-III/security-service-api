from db.mongo_client import Connection
from decouple import config

__dbmanager__ = Connection(config('ROLE_COLLECTION'))

def db_find_active_and_default_roles():
    try:
        roles_cursor = __dbmanager__.collection.find({
            'is_active': True,
            '$or': [{'default_role': {'$exists': True}}, {'default_role': True}]
        })
        
        roles_list = []
        default_role = None
        
        for role in roles_cursor:
            roles_list.append(role)
            if role.get('default_role'):
                default_role = role
        
        return roles_list, default_role
    except Exception as e:
        raise RuntimeError(f'Error al buscar roles activos y predeterminados: {str(e)}')
