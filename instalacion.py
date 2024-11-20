import os
import subprocess
import sys

def crear_entorno_virtual(env_name):
    """
    Crea un entorno virtual llamado env_name.
    """
    print(f"Creando entorno virtual: {env_name}...")
    subprocess.run([sys.executable, '-m', 'venv', env_name])
    print(f"Entorno virtual {env_name} creado exitosamente.")

def instalar_dependencias(env_name):
    """
    Instala las dependencias desde requierements.txt dentro del entorno virtual.
    """
    requierements_file = "requierements.txt"
    if not os.path.exists(requierements_file):
        print(f"Error: No se encontró {requierements_file}.")
        sys.exit(1)
    
    print(f"Instalando dependencias desde {requierements_file}...")
    pip_executable = os.path.join(env_name, 'Scripts', 'pip') if os.name == 'nt' else os.path.join(env_name, 'bin', 'pip')
    subprocess.run([pip_executable, 'install', '-r', requierements_file])
    print("Dependencias instaladas exitosamente.")

def main():
    env_name = "env_django"
    crear_entorno_virtual(env_name)
    instalar_dependencias(env_name)
    print(f"\nInstalación completada. Para ejecutar el servidor, usa app_run.py.")

if __name__ == "__main__":
    main()
