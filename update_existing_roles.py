#!/usr/bin/env python3
"""
Script para actualizar roles existentes que tienen admin_id null
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

def update_role_admin_id(token, role_id, admin_id):
    """Actualizar el admin_id de un rol específico"""
    url = f"{BASE_URL}/rol/{role_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Solo actualizar el admin_id, mantener el resto igual
    data = {
        "admin_id": admin_id
    }
    
    response = requests.patch(url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"✅ Rol {role_id} actualizado con admin_id: {admin_id}")
        return True
    else:
        print(f"❌ Error actualizando rol {role_id}: {response.status_code} - {response.text}")
        return False

def main():
    print("🔄 Iniciando actualización de roles existentes...")
    
    # 1. Login como admin
    print("🔐 Iniciando sesión como admin...")
    token = login_admin()
    if not token:
        print("❌ No se pudo obtener el token. Saliendo...")
        return
    
    print("✅ Login exitoso")
    
    # 2. Obtener todos los roles
    print("📋 Obteniendo todos los roles...")
    roles = get_all_roles(token)
    if not roles:
        print("❌ No se pudieron obtener los roles. Saliendo...")
        return
    
    print(f"✅ Se obtuvieron {len(roles)} roles")
    
    # 3. Extraer admin_id del token
    import jwt
    try:
        # Decodificar el token (sin verificar la firma para obtener los datos)
        token_data = jwt.decode(token, options={"verify_signature": False})
        admin_id = token_data.get("sub")  # El admin_id está en el campo "sub"
        print(f"🔍 Admin ID del token: {admin_id}")
    except Exception as e:
        print(f"❌ Error decodificando token: {e}")
        return
    
    # 4. Identificar roles que necesitan actualización
    roles_to_update = []
    for role in roles:
        role_admin_id = role.get("admin_id")
        if role_admin_id is None:
            roles_to_update.append(role)
            print(f"📝 Rol '{role['name']}' (ID: {role['_id']}) necesita actualización")
    
    if not roles_to_update:
        print("✅ Todos los roles ya tienen admin_id configurado")
        return
    
    print(f"🔄 Se actualizarán {len(roles_to_update)} roles")
    
    # 5. Actualizar cada rol
    success_count = 0
    for role in roles_to_update:
        role_id = role["_id"]
        role_name = role["name"]
        
        print(f"🔄 Actualizando rol '{role_name}'...")
        if update_role_admin_id(token, role_id, admin_id):
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
