#!/usr/bin/env python3
"""
Script simple para hacer commits de git
"""

import os
import subprocess

def run_git_command(command):
    """Ejecutar comando git"""
    print(f"Ejecutando: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Exitoso: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        return False

def main():
    print("🚀 Creando rama Aaron-Dev02 y haciendo commits...")
    
    # 1. Crear rama
    if not run_git_command("git checkout -b Aaron-Dev02"):
        return
    
    # 2. Agregar archivos
    if not run_git_command("git add ."):
        return
    
    # 3. Hacer commit
    commit_msg = """feat: Simplify role structure by removing redundant fields

- Remove 'app' and 'app_client_id' fields from role model
- Keep only 'admin_id' and 'app_id' for role identification
- Update role controller to use simplified structure
- Update role model constructor and methods
- Update documentation (Postman guide and Swagger)
- Create test scripts for simplified structure
- Maintain backward compatibility with existing functionality

This change simplifies the role data structure while maintaining
all necessary functionality for role management."""
    
    if not run_git_command(f'git commit -m "{commit_msg}"'):
        return
    
    # 4. Verificar estado
    run_git_command("git status")
    run_git_command("git branch")
    
    print("✅ Proceso completado!")

if __name__ == "__main__":
    main()
