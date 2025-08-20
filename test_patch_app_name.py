#!/usr/bin/env python3
"""
Script para probar la actualización del nombre de la aplicación
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

def test_get_apps(token):
    """Probar obtención de apps para obtener un ID válido"""
    print("\n📱 Probando obtención de apps...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/apps", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            apps = data.get('data', [])
            print(f"✅ Apps obtenidas exitosamente. Total: {len(apps)}")
            
            if apps:
                app_id = apps[0].get('_id')
                app_name = apps[0].get('name')
                print(f"📋 Usando app_id: {app_id}")
                print(f"📋 Nombre actual: {app_name}")
                return app_id, app_name
            else:
                print("⚠️ No hay apps disponibles")
                return None, None
        else:
            print(f"❌ Error obteniendo apps: {response.text}")
            return None, None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None, None

def test_patch_app_name(token, app_id, original_name):
    """Probar actualización del nombre de la app"""
    if not app_id:
        print("❌ No hay app_id para actualizar")
        return False
        
    print(f"\n🔄 Probando PATCH /apps/{app_id} - Actualizar nombre")
    
    # Nuevo nombre temporal
    new_name = f"{original_name}-updated"
    
    update_data = {
        "name": new_name
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/apps/{app_id}", 
                                json=update_data, 
                                headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Nombre de app actualizado exitosamente")
            print(f"Respuesta: {json.dumps(data, indent=2)}")
            
            # Verificar que el cambio se aplicó
            updated_app = data.get('data', {})
            if updated_app.get('name') == new_name:
                print("✅ Verificación: El nombre se actualizó correctamente")
            else:
                print("⚠️ Verificación: El nombre no se actualizó como esperado")
            
            return True
        else:
            print(f"❌ Error actualizando nombre: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_patch_app_multiple_fields(token, app_id):
    """Probar actualización de múltiples campos"""
    if not app_id:
        print("❌ No hay app_id para actualizar")
        return False
        
    print(f"\n🔄 Probando PATCH /apps/{app_id} - Múltiples campos")
    
    update_data = {
        "name": "test-multi-update",
        "status": "inactive",
        "redirect_url": "http://localhost:3000/multi-update-callback"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/apps/{app_id}", 
                                json=update_data, 
                                headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Múltiples campos actualizados exitosamente")
            print(f"Respuesta: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"❌ Error actualizando múltiples campos: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_patch_app_duplicate_name(token, app_id):
    """Probar que no se puede usar un nombre que ya existe"""
    print(f"\n🔄 Probando PATCH /apps/{app_id} - Nombre duplicado")
    
    # Intentar usar un nombre que probablemente ya existe
    update_data = {
        "name": "vehiculos"  # Nombre común que probablemente existe
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/apps/{app_id}", 
                                json=update_data, 
                                headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 422:
            data = response.json()
            print("✅ Correctamente rechazado - nombre duplicado")
            print(f"Respuesta: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"⚠️ No se rechazó como esperado: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_patch_app_invalid_name(token, app_id):
    """Probar que no se puede usar un nombre inválido"""
    print(f"\n🔄 Probando PATCH /apps/{app_id} - Nombre inválido")
    
    update_data = {
        "name": "a"  # Nombre muy corto
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/apps/{app_id}", 
                                json=update_data, 
                                headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 422:
            data = response.json()
            print("✅ Correctamente rechazado - nombre inválido")
            print(f"Respuesta: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"⚠️ No se rechazó como esperado: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de actualización de nombre de app")
    print("=" * 60)
    
    # 1. Login
    token = test_admin_login()
    if not token:
        print("❌ No se pudo obtener token. Abortando pruebas.")
        return
    
    # 2. Obtener app_id
    app_id, original_name = test_get_apps(token)
    if not app_id:
        print("❌ No se pudo obtener app_id. Abortando pruebas.")
        return
    
    # 3. Probar actualización de nombre
    test_patch_app_name(token, app_id, original_name)
    
    # 4. Probar actualización de múltiples campos
    test_patch_app_multiple_fields(token, app_id)
    
    # 5. Probar nombre duplicado
    test_patch_app_duplicate_name(token, app_id)
    
    # 6. Probar nombre inválido
    test_patch_app_invalid_name(token, app_id)
    
    print("\n" + "=" * 60)
    print("✅ Pruebas completadas")

if __name__ == "__main__":
    main()
