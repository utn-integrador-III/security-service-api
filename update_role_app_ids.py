#!/usr/bin/env python3
"""
Script para actualizar app_id de roles existentes que lo tienen como null
"""

import requests
import json
from bson import ObjectId

# Configuración
BASE_URL = "http://localhost:5002"
ADMIN_EMAIL = "aaroncontreras1816@gmail.com"
ADMIN_PASSWORD = "123456"

def login_admin():
    """Login como admin para obtener el token"""
    url = f"{BASE_URL}/auth/admin/login"
    data = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()["data"]["token"]
    else:
        print(f"❌ Error en login: {response.status_code} - {response.text}")
        return None

def get_all_roles(token):
    """Obtener todos los roles"""
    url = f"{BASE_URL}/rol"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"❌ Error obteniendo roles: {response.status_code} - {response.text}")
        return []

def get_admin_apps(token):
    """Obtener las apps asociadas al admin"""
    url = f"{BASE_URL}/apps"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"❌ Error obteniendo apps: {response.status_code} - {response.text}")
        return []

def update_role_app_id(token, role_id, app_id):
    """Actualizar el app_id de un rol específico"""
    url = f"{BASE_URL}/rol/{role_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Solo actualizar el app_id, mantener el resto igual
    data = {
        "app_id": app_id
    }
    
    response = requests.patch(url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"✅ Rol {role_id} actualizado con app_id: {app_id}")
        return True
    else:
        print(f"❌ Error actualizando rol {role_id}: {response.status_code} - {response.text}")
        return False

def main():
    print("🔄 Iniciando actualización de app_id en roles existentes...")
    
    # 1. Login como admin
    print("🔐 Iniciando sesión como admin...")
    token = login_admin()
    if not token:
        print("❌ No se pudo obtener el token. Saliendo...")
        return
    
    print("✅ Login exitoso")
    
    # 2. Obtener todas las apps del admin
    print("📋 Obteniendo apps del admin...")
    apps = get_admin_apps(token)
    if not apps:
        print("❌ No se pudieron obtener las apps. Saliendo...")
        return
    
    print(f"✅ Se obtuvieron {len(apps)} apps")
    
    # Usar la primera app como app_id por defecto
    default_app_id = apps[0]["_id"]
    print(f"🔍 App ID por defecto: {default_app_id}")
    
    # 3. Obtener todos los roles
    print("📋 Obteniendo todos los roles...")
    roles = get_all_roles(token)
    if not roles:
        print("❌ No se pudieron obtener los roles. Saliendo...")
        return
    
    print(f"✅ Se obtuvieron {len(roles)} roles")
    
    # 4. Identificar roles que necesitan actualización de app_id
    roles_to_update = []
    for role in roles:
        role_app_id = role.get("app_id")
        if role_app_id is None:
            roles_to_update.append(role)
            print(f"📝 Rol '{role['name']}' (ID: {role['_id']}) necesita app_id")
    
    if not roles_to_update:
        print("✅ Todos los roles ya tienen app_id configurado")
        return
    
    print(f"🔄 Se actualizarán {len(roles_to_update)} roles")
    
    # 5. Actualizar cada rol
    success_count = 0
    for role in roles_to_update:
        role_id = role["_id"]
        role_name = role["name"]
        
        print(f"🔄 Actualizando rol '{role_name}'...")
        if update_role_app_id(token, role_id, default_app_id):
            success_count += 1
    
    print(f"\n📊 Resumen:")
    print(f"   - Roles procesados: {len(roles_to_update)}")
    print(f"   - Roles actualizados exitosamente: {success_count}")
    print(f"   - Roles con errores: {len(roles_to_update) - success_count}")
    
    if success_count == len(roles_to_update):
        print("✅ Todos los roles fueron actualizados exitosamente")
    else:
        print("⚠️  Algunos roles no pudieron ser actualizados")

if __name__ == "__main__":
    main()
