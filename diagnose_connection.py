#!/usr/bin/env python3
"""
Script para diagnosticar problemas de conectividad entre frontend y backend
"""
import requests
import socket
import sys

def check_server_status():
    """
    Verificar si el servidor está corriendo
    """
    print("🔍 Verificando estado del servidor...")
    
    try:
        # Verificar si el puerto 5002 está abierto
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 5002))
        sock.close()
        
        if result == 0:
            print("✅ Puerto 5002 está abierto")
        else:
            print("❌ Puerto 5002 está cerrado")
            return False
    except Exception as e:
        print(f"❌ Error verificando puerto: {e}")
        return False
    
    # Probar endpoint de health
    try:
        response = requests.get("http://localhost:5002/health", timeout=5)
        if response.status_code == 200:
            print("✅ Endpoint /health responde correctamente")
            return True
        else:
            print(f"❌ Endpoint /health responde con status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        return False
    except Exception as e:
        print(f"❌ Error probando /health: {e}")
        return False

def test_cors():
    """
    Probar si CORS está configurado correctamente
    """
    print("\n🔍 Verificando configuración CORS...")
    
    try:
        # Simular una petición desde el frontend
        headers = {
            'Origin': 'http://localhost:3000',
            'Content-Type': 'application/json'
        }
        
        response = requests.get("http://localhost:5002/health", headers=headers)
        
        # Verificar headers CORS
        cors_headers = [
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Methods',
            'Access-Control-Allow-Headers'
        ]
        
        for header in cors_headers:
            if header in response.headers:
                print(f"✅ {header}: {response.headers[header]}")
            else:
                print(f"⚠️  {header} no encontrado")
        
        return True
    except Exception as e:
        print(f"❌ Error probando CORS: {e}")
        return False

def test_delete_endpoint():
    """
    Probar el endpoint de eliminar roles
    """
    print("\n🔍 Probando endpoint DELETE /rol...")
    
    try:
        # Primero hacer login
        login_data = {
            "email": "contrerasaaron447111111@est.utn.ac.cr",
            "password": "Secret123*"
        }
        
        login_response = requests.post(
            "http://localhost:5002/auth/admin/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code != 200:
            print(f"❌ Error en login: {login_response.status_code}")
            return False
        
        token = login_response.json()['data']['token']
        print("✅ Login exitoso")
        
        # Crear un rol para luego eliminarlo
        role_data = {
            "name": "TestDeleteRole",
            "description": "Rol para probar eliminación",
            "permissions": ["read"]
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        create_response = requests.post(
            "http://localhost:5002/rol",
            json=role_data,
            headers=headers
        )
        
        if create_response.status_code != 201:
            print(f"❌ Error creando rol: {create_response.status_code}")
            return False
        
        print("✅ Rol creado exitosamente")
        
        # Probar eliminar el rol
        delete_data = {
            "role_name": "TestDeleteRole"
        }
        
        delete_response = requests.delete(
            "http://localhost:5002/rol",
            json=delete_data,
            headers=headers
        )
        
        print(f"📊 Respuesta DELETE: {delete_response.status_code}")
        
        if delete_response.status_code == 200:
            print("✅ Endpoint DELETE /rol funciona correctamente")
            return True
        else:
            print(f"❌ Error en DELETE: {delete_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando endpoint: {e}")
        return False

def main():
    """
    Función principal de diagnóstico
    """
    print("🚀 Iniciando diagnóstico de conectividad...\n")
    
    # Verificar servidor
    if not check_server_status():
        print("\n💡 SOLUCIÓN: El servidor no está corriendo")
        print("   Ejecuta: python app.py")
        return
    
    # Verificar CORS
    test_cors()
    
    # Probar endpoint
    test_delete_endpoint()
    
    print("\n" + "="*50)
    print("📋 RESUMEN DE DIAGNÓSTICO:")
    print("1. Verifica que el servidor esté corriendo en puerto 5002")
    print("2. Verifica que el frontend esté corriendo en puerto 3000")
    print("3. Verifica que no haya firewall bloqueando las conexiones")
    print("4. Verifica que las URLs en el frontend sean correctas")

if __name__ == "__main__":
    main()
