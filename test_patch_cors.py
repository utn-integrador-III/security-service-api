#!/usr/bin/env python3
"""
Script para probar que las peticiones PATCH funcionan con CORS
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
                print(f"📋 Usando app_id: {app_id}")
                return app_id
            else:
                print("⚠️ No hay apps disponibles")
                return None
        else:
            print(f"❌ Error obteniendo apps: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_patch_app(token, app_id):
    """Probar actualización de app con PATCH"""
    if not app_id:
        print("❌ No hay app_id para actualizar")
        return False
        
    print(f"\n🔄 Probando PATCH /apps/{app_id}")
    
    update_data = {
        "status": "inactive",
        "redirect_url": "http://localhost:3000/updated-callback"
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
            print("✅ App actualizada exitosamente")
            print(f"Respuesta: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"❌ Error actualizando app: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_cors_headers():
    """Probar que los headers CORS incluyen PATCH"""
    print("\n🌐 Probando headers CORS...")
    
    try:
        # Hacer una petición OPTIONS para ver los headers CORS
        response = requests.options(f"{BASE_URL}/apps")
        print(f"Status: {response.status_code}")
        
        # Verificar headers CORS
        cors_headers = {
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin')
        }
        
        print("📋 Headers CORS:")
        for header, value in cors_headers.items():
            print(f"  {header}: {value}")
        
        # Verificar si PATCH está permitido
        if cors_headers.get('Access-Control-Allow-Methods'):
            methods = cors_headers['Access-Control-Allow-Methods']
            if 'PATCH' in methods:
                print("✅ PATCH está permitido en CORS")
                return True
            else:
                print("❌ PATCH NO está permitido en CORS")
                return False
        else:
            print("⚠️ No se encontraron headers CORS")
            return False
            
    except Exception as e:
        print(f"❌ Error probando CORS: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de PATCH con CORS")
    print("=" * 60)
    
    # 1. Probar headers CORS
    cors_ok = test_cors_headers()
    
    # 2. Login
    token = test_admin_login()
    if not token:
        print("❌ No se pudo obtener token. Abortando pruebas.")
        return
    
    # 3. Obtener app_id
    app_id = test_get_apps(token)
    
    # 4. Probar PATCH
    if app_id:
        test_patch_app(token, app_id)
    
    print("\n" + "=" * 60)
    print("✅ Pruebas completadas")
    
    if cors_ok:
        print("🎉 CORS configurado correctamente para PATCH")
    else:
        print("⚠️ Revisar configuración CORS")

if __name__ == "__main__":
    main()
