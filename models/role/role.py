from models.role.db_queries import db_find_active_and_default_roles
import logging
from models.role.db_queries import __dbmanager__
#from models.application.getapp import ApplicationModel

class RoleModel:
    def __init__(self, name, description, permissions, creation_date, mod_date, is_active, default_role, screens, admin_id=None, app_id=None, _id=None):
        self.name = name
        self.description = description
        self.permissions = permissions
        self.creation_date = creation_date
        self.mod_date = mod_date
        self.is_active = is_active
        self.default_role = default_role
        self.screens = screens
        self.admin_id = admin_id
        self.app_id = app_id
        self._id = _id
        
    def to_dict(self):
        return {
            "_id": self._id,
            "name": self.name,
            "description": self.description,
            "permissions": self.permissions,
            "creation_date": self.creation_date,
            "mod_date": self.mod_date,
            "is_active": self.is_active,
            "default_role": self.default_role,
            "screens": self.screens,
            "admin_id": self.admin_id,
            "app_id": self.app_id
        }

    @classmethod
    def find_active_and_default_roles(cls):
        # Fetch active roles and the default role from the database
        try:
            roles, default_role = db_find_active_and_default_roles()
            return roles, default_role
        except Exception as e:
            raise Exception('Error finding active and default roles')

    @classmethod
    def get_by_name(cls, name):
        try:
            result = __dbmanager__.collection.find_one({"name": name})
            if result:
                return cls(
                    _id=result.get("_id"),
                    name=result.get("name"),
                    description=result.get("description"),
                    permissions=result.get("permissions"),
                    creation_date=result.get("creation_date"),
                    mod_date=result.get("mod_date"),
                    is_active=result.get("is_active"),
                    default_role=result.get("default_role"),
                    screens=result.get("screens"),
                    admin_id=result.get("admin_id"),
                    app_id=result.get("app_id")
                )
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to get rol by name: " + str(ex))

    @classmethod
    def list(cls, filters=None):
        """
        List all roles with optional filters
        """
        try:
            query = {}
            if filters:
                if filters.get('is_active') is not None:
                    query['is_active'] = filters['is_active']
                if filters.get('app'):
                    query['app'] = filters['app']
                if filters.get('app_client_id'):
                    query['app_client_id'] = filters['app_client_id']
            
            results = __dbmanager__.collection.find(query)
            roles = []
            
            for result in results:
                role = cls(
                    _id=result.get("_id"),
                    name=result.get("name"),
                    description=result.get("description"),
                    permissions=result.get("permissions"),
                    creation_date=result.get("creation_date"),
                    mod_date=result.get("mod_date"),
                    is_active=result.get("is_active"),
                    default_role=result.get("default_role"),
                    screens=result.get("screens"),
                    admin_id=result.get("admin_id"),
                    app_id=result.get("app_id")
                )
                roles.append(role)
            
            return roles
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to list roles: " + str(ex))
    

    @classmethod
    def create(cls, role_data):
        try:
            result = __dbmanager__.create_data(role_data)
            if result.inserted_id:
                role_data["_id"] = result.inserted_id
                return cls(**role_data)
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Error creating role: " + str(ex))
        
    #Meotod para agregar screens
    @classmethod
    def add_screens(cls, role_name, client_id, new_screens):
        try:
            if not isinstance(new_screens, list):
                raise ValueError("Screens must be a list of strings")

            # Buscar rol 
            existing_role = __dbmanager__.find_one({"name": role_name, "app_id": client_id})
            if not existing_role:
                return None  # No existe el rol
            

            result = __dbmanager__.collection.update_one(
                {"name": role_name, "app_id": client_id},
                {#Para poder seguir agregando sin que se borren existentes
                    "$addToSet": {
                        "screens": {"$each": new_screens}
                    }
                    
                }
            )

            if result.modified_count == 0:
             # No se agregó nada, las screens ya estaban
                return "DUPLICATE"

            updated_role = __dbmanager__.find_one({"name": role_name, "app_id": client_id})
            return cls(
                _id=updated_role.get("_id"),
                name=updated_role.get("name"),
                description=updated_role.get("description"),
                permissions=updated_role.get("permissions"),
                creation_date=updated_role.get("creation_date"),
                mod_date=updated_role.get("mod_date"),
                is_active=updated_role.get("is_active"),
                default_role=updated_role.get("default_role"),
                screens=updated_role.get("screens"),
                admin_id=updated_role.get("admin_id"),
                app_id=updated_role.get("app_id")
            )
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to add screens: " + str(ex))

    

    @classmethod
    def delete_by_name_and_client_id(cls, role_name, client_id):
        try:
            result = __dbmanager__.collection.delete_one({
                "name": role_name,
                "app_id": client_id
            })
            return result.deleted_count > 0
        except Exception as e:
            logging.exception(e)
            raise Exception(f"Error deleting role: {str(e)}")
    
    #para obtener el rol por nombre y idapp
    @classmethod
    def get_by_name_and_client_id(cls, name, client_id):
        try:
            result = __dbmanager__.find_one({"name": name, "app_id": client_id})
            if result:
                return cls(
                    _id=result.get("_id"),
                    name=result.get("name"),
                    description=result.get("description"),
                    permissions=result.get("permissions"),
                    creation_date=result.get("creation_date"),
                    mod_date=result.get("mod_date"),
                    is_active=result.get("is_active"),
                    default_role=result.get("default_role"),
                    screens=result.get("screens"),
                    admin_id=result.get("admin_id"),
                    app_id=result.get("app_id")
                )
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to get role by name and app_id: " + str(ex))

    @classmethod
    def get_by_id(cls, role_id):
        """Obtener rol por ID"""
        try:
            from bson import ObjectId
            result = __dbmanager__.collection.find_one({"_id": ObjectId(role_id)})
            if result:
                return cls(
                    _id=result.get("_id"),
                    name=result.get("name"),
                    description=result.get("description"),
                    permissions=result.get("permissions"),
                    creation_date=result.get("creation_date"),
                    mod_date=result.get("mod_date"),
                    is_active=result.get("is_active"),
                    default_role=result.get("default_role"),
                    screens=result.get("screens"),
                    admin_id=result.get("admin_id"),
                    app_id=result.get("app_id")
                )
            return None
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to get role by ID: " + str(ex))

    @classmethod
    def update(cls, role_id, update_data):
        """Actualizar rol por ID"""
        try:
            from bson import ObjectId
            from datetime import datetime
            
            # Preparar los campos a actualizar
            update_fields = {}
            
            if 'name' in update_data:
                name = update_data['name'].strip()
                if not name or len(name) < 2:
                    raise ValueError("Role name must be at least 2 characters long")
                
                # Verificar que el nuevo nombre no exista ya (excepto para el rol actual)
                existing_role = __dbmanager__.collection.find_one({
                    "name": name,
                    "_id": {"$ne": ObjectId(role_id)}
                })
                if existing_role:
                    raise ValueError("Role name already exists")
                
                update_fields["name"] = name
            
            if 'description' in update_data:
                description = update_data['description'].strip()
                if description is not None:
                    update_fields["description"] = description
            
            if 'permissions' in update_data:
                permissions = update_data['permissions']
                if not isinstance(permissions, list):
                    raise ValueError("Permissions must be a list")
                update_fields["permissions"] = permissions
            
            if 'is_active' in update_data:
                is_active = update_data['is_active']
                if not isinstance(is_active, bool):
                    raise ValueError("is_active must be a boolean")
                update_fields["is_active"] = is_active
            
            if 'screens' in update_data:
                screens = update_data['screens']
                if not isinstance(screens, list):
                    raise ValueError("Screens must be a list")
                update_fields["screens"] = screens
            
            if 'admin_id' in update_data:
                admin_id = update_data['admin_id']
                if admin_id is not None:
                    # Mantener como string
                    update_fields["admin_id"] = str(admin_id)
                else:
                    # Si es None, permitir establecer admin_id como null
                    update_fields["admin_id"] = None
            

            
            if 'app_id' in update_data:
                app_id = update_data['app_id']
                if app_id is not None:
                    # Convertir a ObjectId si es string
                    if isinstance(app_id, str):
                        app_id = ObjectId(app_id)
                    update_fields["app_id"] = app_id
                else:
                    # Si es None, permitir establecer app_id como null
                    update_fields["app_id"] = None
            
            # Siempre actualizar la fecha de modificación
            update_fields["mod_date"] = datetime.utcnow()
            
            # Si no hay campos para actualizar, retornar error
            if not update_fields:
                raise ValueError("No valid fields to update")
            
            # Actualizar en la base de datos
            result = __dbmanager__.collection.update_one(
                {"_id": ObjectId(role_id)},
                {"$set": update_fields}
            )
            
            if result.modified_count == 0:
                return None  # No se actualizó nada
            
            # Retornar el rol actualizado
            return cls.get_by_id(role_id)
            
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Failed to update role: " + str(ex))

