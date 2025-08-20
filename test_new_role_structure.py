#!/usr/bin/env python3
"""
Script para probar la nueva estructura de roles sin valores "default"
"""

import requests
import json

# Configuración
BASE_URL = "http://localhost:5002"

def test_admin_login():
    """Probar login de admin para obtener token"""
    print("🔐 Probando login de admin...")
    
    login_data = {
        "email": "contrerasaaron447111111@est.utn.ac.cr",
        "password": "123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/admin/login", json=login_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('data', {}).get('token')
            print(f"✅ Login exitoso. Token obtenido: {token[:50]}...")
            return token
        else:
            print(f"❌ Error en login: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_create_role_with_real_app_data(token):
    """Probar creación de rol con datos reales de la app"""
    print("\n📝 Probando creación de rol con datos reales de la app...")
    
    role_data = {
        "name": "TestRoleRealAppData",
        "description": "Rol de prueba con datos reales de la app",
        "permissions": ["Read", "Write", "Delete", "Update"]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/rol", json=role_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Rol creado exitosamente")
            print(f"Respuesta completa: {json.dumps(data, indent=2)}")
            
            # Verificar que no hay valores "default"
            role_info = data.get('data', {})
            app = role_info.get('app')
            app_client_id = role_info.get('app_client_id')
            
            print(f"\n📊 Verificación de datos:")
            print(f"  - app: '{app}' (no debe ser 'default')")
            print(f"  - app_client_id: '{app_client_id}' (no debe ser 'default')")
            print(f"  - admin_id: {role_info.get('admin_id')}")
            print(f"  - app_id: {role_info.get('app_id')}")
            
            if app != "default" and app_client_id != "default":
                print("✅ Valores correctos - no hay 'default'")
                return data.get('data', {}).get('name')
            else:
                print("❌ Error: Se encontraron valores 'default'")
                return None
        else:
            print(f"❌ Error creando rol: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_get_roles(token):
    """Probar obtención de roles"""
    print("\n📋 Probando obtención de roles...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/rol", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Roles obtenidos exitosamente")
            print(f"Total de roles: {len(data.get('data', []))}")
            
            # Mostrar estructura del primer rol
            roles = data.get('data', [])
            if roles:
                first_role = roles[0]
                print(f"\n📊 Estructura del primer rol:")
                print(json.dumps(first_role, indent=2, default=str))
                
                # Verificar que no hay valores "default"
                app = first_role.get('app')
                app_client_id = first_role.get('app_client_id')
                
                if app != "default" and app_client_id != "default":
                    print("✅ Roles existentes también tienen valores correctos")
                else:
                    print("⚠️  Roles existentes tienen valores 'default'")
            
            return True
        else:
            print(f"❌ Error obteniendo roles: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_delete_role(token, role_name):
    """Probar eliminación de rol"""
    if not role_name:
        print("❌ No hay rol para eliminar")
        return False
        
    print(f"\n🗑️ Probando eliminación del rol: {role_name}")
    
    delete_data = {
        "role_name": role_name
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.delete(f"{BASE_URL}/rol", json=delete_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Rol eliminado exitosamente")
            return True
        else:
            print(f"❌ Error eliminando rol: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de nueva estructura de roles (sin valores 'default')")
    print("=" * 70)
    
    # 1. Login
    token = test_admin_login()
    if not token:
        print("❌ No se pudo obtener token. Abortando pruebas.")
        return
    
    # 2. Crear rol con datos reales
    role_name = test_create_role_with_real_app_data(token)
    
    # 3. Obtener roles
    test_get_roles(token)
    
    # 4. Eliminar rol de prueba
    if role_name:
        test_delete_role(token, role_name)
    
    print("\n" + "=" * 70)
    print("✅ Pruebas completadas")

if __name__ == "__main__":
    main()
