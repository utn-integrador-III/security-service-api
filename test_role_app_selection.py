#!/usr/bin/env python3
"""
Script para probar que la creación de roles ahora funciona correctamente
con la aplicación específica seleccionada
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5002"

def login_admin():
    """Hacer login como admin para obtener token"""
    try:
        login_url = f"{BASE_URL}/auth/admin/login"
        login_data = {
            "email": "contrerasaaron447111111@est.utn.ac.cr",
            "password": "Secret123*"
        }
        
        print("🔐 Haciendo login como admin...")
        response = requests.post(login_url, json=login_data, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            token = response.json()['data']['token']
            admin_id = response.json()['data']['admin_id']
            print("✅ Login exitoso")
            return token, admin_id
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"Response: {response.text}")
            return None, None
    except Exception as e:
        print(f"❌ Error en login: {str(e)}")
        return None, None

def get_admin_apps(token):
    """Obtener las aplicaciones del admin"""
    try:
        apps_url = f"{BASE_URL}/apps"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        print("📱 Obteniendo aplicaciones del admin...")
        response = requests.get(apps_url, headers=headers)
        
        if response.status_code == 200:
            apps = response.json()['data']
            print(f"✅ Aplicaciones encontradas: {len(apps)}")
            for app in apps:
                print(f"   - {app['name']} (ID: {app['_id']})")
            return apps
        else:
            print(f"❌ Error obteniendo apps: {response.status_code}")
            print(f"Response: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Error obteniendo apps: {str(e)}")
        return []

def create_role_for_specific_app(token, admin_id, app_id, app_name):
    """Crear un rol para una aplicación específica"""
    try:
        role_url = f"{BASE_URL}/rol"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Datos del rol
        role_data = {
            "name": f"Test Role {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "description": f"Rol de prueba para la aplicación {app_name}",
            "permissions": ["read", "write", "update"],
            "admin_id": admin_id,
            "app_id": app_id
        }
        
        print(f"\n🔧 Creando rol para la aplicación: {app_name}")
        print(f"   App ID: {app_id}")
        print(f"   Role data: {json.dumps(role_data, indent=2)}")
        
        response = requests.post(role_url, json=role_data, headers=headers)
        
        print(f"📊 Respuesta:")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            created_role = response.json()['data']
            print("✅ Rol creado exitosamente!")
            print(f"   Role ID: {created_role['_id']}")
            print(f"   Role Name: {created_role['name']}")
            print(f"   App ID: {created_role['app_id']}")
            print(f"   Admin ID: {created_role['admin_id']}")
            return created_role
        else:
            print(f"❌ Error creando rol: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creando rol: {str(e)}")
        return None

def verify_role_creation(token, app_id):
    """Verificar que el rol se creó correctamente"""
    try:
        roles_url = f"{BASE_URL}/rol"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        print(f"\n🔍 Verificando roles para la aplicación {app_id}...")
        response = requests.get(roles_url, headers=headers)
        
        if response.status_code == 200:
            roles = response.json()['data']
            app_roles = [role for role in roles if role.get('app_id') == app_id]
            print(f"✅ Roles encontrados para la aplicación: {len(app_roles)}")
            for role in app_roles:
                print(f"   - {role['name']} (ID: {role['_id']})")
            return app_roles
        else:
            print(f"❌ Error obteniendo roles: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error verificando roles: {str(e)}")
        return []

def main():
    print("🧪 Probando creación de roles con aplicación específica...")
    print("=" * 60)
    
    # 1. Login como admin
    token, admin_id = login_admin()
    if not token:
        return
    
    # 2. Obtener aplicaciones del admin
    apps = get_admin_apps(token)
    if not apps:
        print("❌ No se encontraron aplicaciones")
        return
    
    # 3. Crear roles para cada aplicación
    created_roles = []
    for app in apps:
        role = create_role_for_specific_app(token, admin_id, app['_id'], app['name'])
        if role:
            created_roles.append(role)
    
    # 4. Verificar que los roles se crearon correctamente
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    for app in apps:
        app_roles = verify_role_creation(token, app['_id'])
        print(f"\n📱 Aplicación: {app['name']}")
        print(f"   Roles creados: {len(app_roles)}")
    
    print(f"\n✅ Total de roles creados: {len(created_roles)}")
    print("🎉 Prueba completada exitosamente!")

if __name__ == "__main__":
    main()
