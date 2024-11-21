import subprocess
import os
import sys

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
    Crea un entorno virtual llamado 'env_django' y lo configura.
    """
    try:
        print("Creando el entorno virtual 'env_django'...")
        subprocess.run([sys.executable, '-m', 'venv', 'env_django'], check=True)
        print("Entorno virtual creado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al crear el entorno virtual: {e}")
        input("Presione Enter para salir...")
        exit(1)

def instalar_dependencias_entorno_virtual():
    """
    Instala las dependencias desde requirements.txt dentro del entorno virtual.
    """
    try:
        print("Instalando dependencias en el entorno virtual...")
        # Ruta al ejecutable pip dentro del entorno virtual
        pip_executable = os.path.join('env_django', 'Scripts', 'pip.exe') if os.name == 'nt' else os.path.join('env_django', 'bin', 'pip')

        # Instalar las dependencias usando el pip del entorno virtual
        subprocess.run([pip_executable, 'install', '-r', 'requierements.txt'], check=True)
        print("Dependencias instaladas correctamente en el entorno virtual.")
    except subprocess.CalledProcessError as e:
        print(f"Error al instalar dependencias en el entorno virtual: {e}")
        input("Presione Enter para salir...")
        exit(1)

def main():
    instalar_dependencias_globales()
    crear_entorno_virtual()
    instalar_dependencias_entorno_virtual()
    print("\nInstalación completada con éxito.")
    input("Presione Enter para salir...")

if __name__ == "__main__":
    main()
