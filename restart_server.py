#!/usr/bin/env python3
"""
Script para reiniciar el servidor Flask
"""
import os
import subprocess
import time
import requests

def check_server():
    """
    Verificar si el servidor está corriendo
    """
    try:
        response = requests.get("http://localhost:5002/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def restart_server():
    """
    Reiniciar el servidor
    """
    print("🔄 Reiniciando el servidor...")
    
    # Buscar procesos de Python que estén corriendo el servidor
    try:
        # En Windows
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq python.exe", "/FO", "CSV"],
            capture_output=True, text=True
        )
        
        if "python.exe" in result.stdout:
            print("⚠️  Servidor Python detectado, intentando detener...")
            subprocess.run(["taskkill", "/F", "/IM", "python.exe"], capture_output=True)
            time.sleep(2)
    except:
        pass
    
    # Iniciar el servidor
    print("🚀 Iniciando servidor...")
    try:
        subprocess.Popen(["python", "run_server.py"], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        
        # Esperar a que el servidor inicie
        print("⏳ Esperando a que el servidor inicie...")
        for i in range(10):
            time.sleep(1)
            if check_server():
                print("✅ Servidor iniciado correctamente")
                return True
            print(f"   Intento {i+1}/10...")
        
        print("❌ No se pudo iniciar el servidor")
        return False
        
    except Exception as e:
        print(f"❌ Error iniciando servidor: {str(e)}")
        return False

def test_endpoints():
    """
    Probar los endpoints después del reinicio
    """
    print("\n🧪 Probando endpoints...")
    
    # Probar health
    try:
        response = requests.get("http://localhost:5002/health")
        print(f"✅ Health endpoint: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint: {str(e)}")
        return
    
    # Probar login
    try:
        login_response = requests.post(
            "http://localhost:5002/auth/admin/login",
            json={
                "email": "contrerasaaron447111111@est.utn.ac.cr",
                "password": "Secret123*"
            },
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Login endpoint: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token = login_response.json()['data']['token']
            
            # Probar roles
            roles_response = requests.get(
                "http://localhost:5002/rol",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
            )
            print(f"✅ Roles endpoint: {roles_response.status_code}")
            
            if roles_response.status_code == 200:
                print("🎉 ¡Todos los endpoints funcionan correctamente!")
            else:
                print(f"❌ Roles endpoint error: {roles_response.text}")
        else:
            print(f"❌ Login endpoint error: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Error probando endpoints: {str(e)}")

if __name__ == "__main__":
    print("🚀 Script de reinicio del servidor\n")
    
    if check_server():
        print("✅ Servidor ya está corriendo")
    else:
        print("❌ Servidor no está corriendo")
        if restart_server():
            test_endpoints()
        else:
            print("💡 Para iniciar manualmente, ejecuta: python run_server.py")
