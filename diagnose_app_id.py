#!/usr/bin/env python3
"""
Script para diagnosticar por qué no se está asignando el app_id automáticamente
"""

import requests
import json
from datetime import datetime

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

def get_admin_apps(token):
    """Obtener las apps del admin"""
    url = f"{BASE_URL}/apps"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"❌ Error obteniendo apps: {response.status_code} - {response.text}")
        return []

def test_app_id_assignment(token, admin_id):
    """Probar la asignación automática de app_id"""
    url = f"{BASE_URL}/rol"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Datos del rol de prueba
    role_data = {
        "name": f"Test AppID {datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "description": "Rol para probar asignación automática de app_id",
        "permissions": ["Read", "Write"],
        "admin_id": admin_id,
        "created_by": admin_id
    }
    
    print(f"🚀 Creando rol con datos:")
    print(json.dumps(role_data, indent=2))
    
    response = requests.post(url, json=role_data, headers=headers)
    
    if response.status_code == 201:
        created_role = response.json()["data"]
        print("✅ Rol creado exitosamente!")
        print("📋 Estructura del rol creado:")
        print(json.dumps(created_role, indent=2, default=str))
        
        # Verificar app_id
        app_id = created_role.get("app_id")
        if app_id:
            print(f"✅ App ID asignado correctamente: {app_id}")
        else:
            print("❌ App ID NO fue asignado")
        
        return created_role
    else:
        print(f"❌ Error creando rol: {response.status_code} - {response.text}")
        return None

def main():
    print("🔍 Diagnóstico de asignación automática de app_id...")
    
    # 1. Login como admin
    print("\n🔐 Iniciando sesión como admin...")
    token = login_admin()
    if not token:
        print("❌ No se pudo obtener el token. Saliendo...")
        return
    
    print("✅ Login exitoso")
    
    # 2. Extraer admin_id del token
    import jwt
    try:
        token_data = jwt.decode(token, options={"verify_signature": False})
        admin_id = token_data.get("sub")
        print(f"🔍 Admin ID del token: {admin_id}")
    except Exception as e:
        print(f"❌ Error decodificando token: {e}")
        return
    
    # 3. Obtener apps del admin
    print("\n📋 Obteniendo apps del admin...")
    apps = get_admin_apps(token)
    if not apps:
        print("❌ No se pudieron obtener las apps")
        return
    
    print(f"✅ Se obtuvieron {len(apps)} apps:")
    for i, app in enumerate(apps):
        print(f"  {i+1}. {app['name']} (ID: {app['_id']})")
    
    # 4. Probar creación de rol con app_id automático
    print("\n🔄 Probando creación de rol con app_id automático...")
    created_role = test_app_id_assignment(token, admin_id)
    
    if created_role:
        print("\n🎉 Diagnóstico completado")
        app_id = created_role.get("app_id")
        if app_id:
            print("✅ El app_id se está asignando correctamente")
        else:
            print("❌ El app_id NO se está asignando")
    else:
        print("\n❌ El diagnóstico falló")

if __name__ == "__main__":
    main()
