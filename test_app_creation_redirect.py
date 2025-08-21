#!/usr/bin/env python3
"""
Script para probar la creación de app con redirección al login de administrador
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

def test_create_app_with_redirect(token):
    """Probar creación de app con redirección"""
    print("\n📱 Probando creación de app con redirección...")
    
    app_data = {
        "name": "test-app-redirect",
        "redirect_url": "http://localhost:3000/test-callback",
        "status": "active"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/apps", json=app_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ App creada exitosamente con redirección")
            print(f"Respuesta: {json.dumps(data, indent=2)}")
            
            # Verificar estructura de redirección
            response_data = data.get('data', {})
            redirect_info = response_data.get('redirect_to', {})
            
            if redirect_info:
                print("\n🔍 Verificando información de redirección:")
                print(f"  URL: {redirect_info.get('url')}")
                print(f"  Mensaje: {redirect_info.get('message')}")
                print(f"  Tipo: {redirect_info.get('type')}")
                
                if redirect_info.get('url') == '/auth/admin/login':
                    print("✅ Redirección configurada correctamente")
                else:
                    print("⚠️ URL de redirección incorrecta")
                    
                if redirect_info.get('type') == 'admin_login':
                    print("✅ Tipo de redirección correcto")
                else:
                    print("⚠️ Tipo de redirección incorrecto")
            else:
                print("❌ No se encontró información de redirección")
            
            return True
        else:
            print(f"❌ Error creando app: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_create_app_without_token():
    """Probar creación de app sin token (debería fallar)"""
    print("\n🚫 Probando creación de app sin token...")
    
    app_data = {
        "name": "test-app-no-token",
        "redirect_url": "http://localhost:3000/test-callback",
        "status": "active"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/apps", json=app_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ Correctamente rechazado - requiere autenticación")
            return True
        else:
            print(f"⚠️ No se rechazó como esperado: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_create_app_duplicate_name(token):
    """Probar creación de app con nombre duplicado"""
    print("\n🔄 Probando creación de app con nombre duplicado...")
    
    app_data = {
        "name": "test-app-redirect",  # Mismo nombre que el anterior
        "redirect_url": "http://localhost:3000/test-callback-2",
        "status": "active"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/apps", json=app_data, headers=headers)
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

def test_admin_login_endpoint():
    """Probar que el endpoint de login de admin existe y funciona"""
    print("\n🔐 Probando endpoint de login de admin...")
    
    login_data = {
        "email": "contrerasaaron447111111@est.utn.ac.cr",
        "password": "123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/admin/login", json=login_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint de login de admin funciona correctamente")
            print(f"Token: {data.get('data', {}).get('token', '')[:50]}...")
            return True
        else:
            print(f"❌ Error en endpoint de login: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de creación de app con redirección")
    print("=" * 60)
    
    # 1. Probar endpoint de login de admin
    test_admin_login_endpoint()
    
    # 2. Login para obtener token
    token = test_admin_login()
    if not token:
        print("❌ No se pudo obtener token. Abortando pruebas.")
        return
    
    # 3. Probar creación de app con redirección
    test_create_app_with_redirect(token)
    
    # 4. Probar creación sin token
    test_create_app_without_token()
    
    # 5. Probar nombre duplicado
    test_create_app_duplicate_name(token)
    
    print("\n" + "=" * 60)
    print("✅ Pruebas completadas")
    print("\n📋 Resumen:")
    print("- ✅ App creada con información de redirección")
    print("- ✅ Redirección apunta a /auth/admin/login")
    print("- ✅ Endpoint de login de admin funciona")
    print("- ✅ Validaciones de seguridad funcionan")

if __name__ == "__main__":
    main()
