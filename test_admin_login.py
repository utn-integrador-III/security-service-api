#!/usr/bin/env python3
"""
Script para probar el endpoint de admin login
"""
import requests
import json

def test_admin_login():
    """
    Probar el endpoint de admin login
    """
    url = "http://localhost:5002/auth/admin/login"
    
    # Datos de prueba
    data = {
        "email": "contrerasaaron447111111@est.utn.ac.cr",
        "password": "Secret123*"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("🔍 Probando endpoint de admin login...")
        print(f"URL: {url}")
        print(f"Datos: {json.dumps(data, indent=2)}")
        
        response = requests.post(url, json=data, headers=headers)
        
        print(f"\n📊 Respuesta:")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ ¡ÉXITO! Login exitoso")
            response_data = response.json()
            print(f"Token: {response_data.get('data', {}).get('token', 'No token')[:50]}...")
            print(f"Mensaje: {response_data.get('message', 'No message')}")
        else:
            print("❌ Error en el login")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión. Asegúrate de que el servidor esté corriendo en http://localhost:5002")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

def test_health_endpoint():
    """
    Probar el endpoint de health para verificar que el servidor esté corriendo
    """
    try:
        response = requests.get("http://localhost:5002/health")
        if response.status_code == 200:
            print("✅ Servidor está corriendo correctamente")
            return True
        else:
            print(f"❌ Servidor respondió con status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del endpoint de admin login...\n")
    
    # Primero verificar que el servidor esté corriendo
    if test_health_endpoint():
        print("\n" + "="*50)
        test_admin_login()
    else:
        print("\n💡 Para iniciar el servidor, ejecuta:")
        print("   python run_server.py")
