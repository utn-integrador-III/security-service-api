#!/usr/bin/env python3
"""
Script para simular una petición desde el frontend
"""
import requests
import json

def test_frontend_connection():
    """
    Simular una petición DELETE desde el frontend
    """
    print("🔍 Simulando petición desde el frontend...")
    
    # Headers que enviaría el frontend
    headers = {
        'Origin': 'http://localhost:3000',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token'
    }
    
    # Probar primero el endpoint de health
    try:
        print("📡 Probando endpoint /health...")
        response = requests.get("http://localhost:5002/health", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Headers CORS: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Endpoint /health responde correctamente")
        else:
            print("❌ Endpoint /health no responde correctamente")
            return False
            
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        return False
    
    # Probar una petición DELETE (sin autenticación real)
    try:
        print("\n📡 Probando petición DELETE...")
        delete_data = {
            "role_name": "TestRole"
        }
        
        response = requests.delete(
            "http://localhost:5002/rol",
            json=delete_data,
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Debería devolver 401 (no autorizado) pero no error de CORS
        if response.status_code in [401, 403, 404]:
            print("✅ Petición DELETE llega al servidor (CORS funciona)")
            return True
        else:
            print("❌ Problema con la petición DELETE")
            return False
            
    except Exception as e:
        print(f"❌ Error en petición DELETE: {e}")
        return False

def main():
    """
    Función principal
    """
    print("🚀 Probando conectividad frontend-backend...\n")
    
    if test_frontend_connection():
        print("\n✅ CONECTIVIDAD FUNCIONANDO")
        print("💡 El problema podría estar en:")
        print("   - Token de autenticación inválido")
        print("   - URL incorrecta en el frontend")
        print("   - Servidor no corriendo")
    else:
        print("\n❌ PROBLEMA DE CONECTIVIDAD")
        print("💡 Verifica que:")
        print("   - El servidor esté corriendo en puerto 5002")
        print("   - No haya firewall bloqueando")
        print("   - Las URLs sean correctas")

if __name__ == "__main__":
    main()
