#!/usr/bin/env python3
"""
Script para verificar y corregir la configuración CORS
"""
import os

def check_env_file():
    """
    Verificar si existe el archivo .env y su configuración
    """
    print("🔍 Verificando archivo de configuración...")
    
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ Archivo .env encontrado")
        
        with open(env_file, 'r') as f:
            content = f.read()
            
        if "SECURITY_API_ENVIRONMENT=Development" in content:
            print("✅ Entorno configurado como Development")
        else:
            print("⚠️  Entorno no configurado como Development")
            print("   Agregando configuración...")
            
            # Agregar configuración si no existe
            if "SECURITY_API_ENVIRONMENT" not in content:
                with open(env_file, 'a') as f:
                    f.write("\nSECURITY_API_ENVIRONMENT=Development\n")
                print("✅ Configuración agregada")
    else:
        print("❌ Archivo .env no encontrado")
        print("   Creando archivo .env...")
        
        env_content = """# Configuración del entorno
SECURITY_API_ENVIRONMENT=Development
FLASK_DEBUG=True
FLASK_RUN_HOST=0.0.0.0
SECURITY_SERVICE_PORT=5002
JWT_SECRET_KEY=your-secret-key-here
"""
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print("✅ Archivo .env creado")

def update_cors_config():
    """
    Actualizar la configuración CORS para asegurar que funcione
    """
    print("\n🔍 Actualizando configuración CORS...")
    
    app_content = """from flask import Flask
from swagger_ui import flask_api_doc
from flask_restful import Api
from flask_cors import CORS
from decouple import config
from service import addServiceLayer
import logging

app = Flask(__name__)
app.debug = config('FLASK_DEBUG', cast=bool, default=True)
api = Api(app)
flask_api_doc(app, config_path='./swagger.yml', url_prefix='/api/doc', title='API doc')
logging.basicConfig(level=logging.INFO)

# Configuración CORS mejorada
cors = CORS(app, 
    resources={r"/*": {"origins": "*"}},
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    supports_credentials=True
)

addServiceLayer(api)

if __name__ == "__main__":
    app.run(host=config('FLASK_RUN_HOST', default='0.0.0.0'), 
            port=config('SECURITY_SERVICE_PORT', cast=int, default=5002))
"""
    
    with open('app.py', 'w') as f:
        f.write(app_content)
    
    print("✅ Configuración CORS actualizada")

def main():
    """
    Función principal
    """
    print("🚀 Verificando y corrigiendo configuración CORS...\n")
    
    check_env_file()
    update_cors_config()
    
    print("\n" + "="*50)
    print("✅ CONFIGURACIÓN COMPLETADA")
    print("\n💡 PRÓXIMOS PASOS:")
    print("1. Reinicia el servidor: python app.py")
    print("2. Ejecuta el diagnóstico: python diagnose_connection.py")
    print("3. Prueba desde el frontend")

if __name__ == "__main__":
    main()
