#!/usr/bin/env python3
"""
Script para crear rama y hacer commits de los cambios realizados
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            print(f"✅ {description} completado")
            if result.stdout:
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"❌ Error en {description}: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Excepción en {description}: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando proceso de commits en rama Aaron-Dev02")
    print("=" * 60)
    
    # 1. Crear nueva rama
    if not run_command("git checkout -b Aaron-Dev02", "Creando rama Aaron-Dev02"):
        print("❌ No se pudo crear la rama. Abortando.")
        return
    
    # 2. Agregar todos los archivos modificados
    if not run_command("git add .", "Agregando archivos modificados"):
        print("❌ No se pudieron agregar archivos. Abortando.")
        return
    
    # 3. Verificar estado
    if not run_command("git status", "Verificando estado del repositorio"):
        print("❌ No se pudo verificar estado. Abortando.")
        return
    
    # 4. Hacer commit principal
    commit_message = """feat: Simplify role structure by removing redundant fields

- Remove 'app' and 'app_client_id' fields from role model
- Keep only 'admin_id' and 'app_id' for role identification
- Update role controller to use simplified structure
- Update role model constructor and methods
- Update documentation (Postman guide and Swagger)
- Create test scripts for simplified structure
- Maintain backward compatibility with existing functionality

This change simplifies the role data structure while maintaining
all necessary functionality for role management."""
    
    if not run_command(f'git commit -m "{commit_message}"', "Haciendo commit principal"):
        print("❌ No se pudo hacer commit. Abortando.")
        return
    
    # 5. Verificar rama actual
    if not run_command("git branch", "Verificando rama actual"):
        print("❌ No se pudo verificar rama. Abortando.")
        return
    
    print("\n" + "=" * 60)
    print("✅ Proceso completado exitosamente")
    print("📋 Resumen de cambios:")
    print("  - Rama creada: Aaron-Dev02")
    print("  - Estructura de roles simplificada")
    print("  - Documentación actualizada")
    print("  - Scripts de prueba creados")

if __name__ == "__main__":
    main()
