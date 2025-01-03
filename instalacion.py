import subprocess
import os
import sys
import getpass  # Para obtener el nombre del usuario actual

# Directorio compartido para los entornos virtuales
SHARED_ENV_DIR = "C:\\envs"

def obtener_nombre_entorno_virtual():
    """
    Genera el nombre del entorno virtual basado en el usuario activo.
    """
    USERNAME = getpass.getuser()
    return f"env_django_{USERNAME}"  # Nombre del entorno virtual para el usuario

def instalar_dependencias_globales():
    """
    Instala PyInstaller y Django en el entorno global.
    """
    try:
        print("Instalando PyInstaller y Django en el entorno global...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller', 'django'], check=True)
        print("Dependencias globales instaladas correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al instalar dependencias globales: {e}")
        input("Presione Enter para salir...")
        exit(1)

def crear_entorno_virtual():
    """
    Crea un entorno virtual específico para el usuario actual.
    """
    try:
        # Crear el directorio compartido si no existe
        if not os.path.exists(SHARED_ENV_DIR):
            print(f"Creando directorio compartido en: {SHARED_ENV_DIR}")
            os.makedirs(SHARED_ENV_DIR)

        # Obtener el nombre y ruta del entorno virtual
        env_name = obtener_nombre_entorno_virtual()
        env_path = os.path.join(SHARED_ENV_DIR, env_name)

        if not os.path.exists(env_path):
            print(f"Creando el entorno virtual '{env_path}'...")
            subprocess.run([sys.executable, '-m', 'venv', env_path], check=True)
            print("Entorno virtual creado correctamente.")
        else:
            print(f"El entorno virtual '{env_path}' ya existe.")
        return env_path
    except subprocess.CalledProcessError as e:
        print(f"Error al crear el entorno virtual: {e}")
        input("Presione Enter para salir...")
        exit(1)

def instalar_dependencias_entorno_virtual(env_path):
    """
    Instala las dependencias desde requirements.txt dentro del entorno virtual.
    """
    try:
        print("Instalando dependencias en el entorno virtual...")
        # Ruta al ejecutable pip dentro del entorno virtual
        pip_executable = os.path.join(env_path, 'Scripts', 'pip.exe') if os.name == 'nt' else os.path.join(env_path, 'bin', 'pip')

        # Instalar las dependencias usando el pip del entorno virtual
        subprocess.run([pip_executable, 'install', '-r', 'requirements.txt'], check=True)
        print("Dependencias instaladas correctamente en el entorno virtual.")
    except subprocess.CalledProcessError as e:
        print(f"Error al instalar dependencias en el entorno virtual: {e}")
        input("Presione Enter para salir...")
        exit(1)

def main():
    """
    Ejecuta el proceso completo de instalación.
    """
    instalar_dependencias_globales()
    env_path = crear_entorno_virtual()
    instalar_dependencias_entorno_virtual(env_path)
    print("\nInstalación completada con éxito.")
    input("Presione Enter para salir...")

if __name__ == "__main__":
    main()
