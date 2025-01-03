from PyInstaller.utils.hooks import copy_metadata
import subprocess
import threading
import webbrowser
import os
import time
import getpass

datas = copy_metadata("django")

def obtener_nombre_entorno_virtual():
    """
    Genera el nombre del entorno virtual basado en el usuario activo.
    """
    USERNAME = getpass.getuser()
    return f"env_django_{USERNAME}"  # Nombre del entorno virtual para el usuario

def configurar_entorno_virtual(env_path):
    """
    Configura las variables de entorno para usar el entorno virtual.
    """
    os.environ["VIRTUAL_ENV"] = env_path
    bin_path = os.path.join(env_path, 'Scripts' if os.name == 'nt' else 'bin')
    os.environ["PATH"] = f"{bin_path};{os.environ['PATH']}"

def run_django_server(env_path):
    """
    Ejecuta el servidor Django desde el entorno virtual.
    """
    try:
        configurar_entorno_virtual(env_path)
        command = "python manage.py runserver"
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el servidor Django: {e}")
    except Exception as ex:
        print(f"Error inesperado: {ex}")
    finally:
        input("Presione Enter para salir...")

def lanzar_navegador():
    """
    Abre el navegador web en la dirección del servidor Django.
    """
    url = "http://127.0.0.1:8000"
    webbrowser.open(url)

def main():
    try:
        # Obtener el entorno virtual del usuario actual
        USERNAME = getpass.getuser()
        env_name = f"env_django_{USERNAME}"  # Basado en el usuario actual
        env_path = os.path.join("C:\\envs", env_name)  # Ruta compartida del entorno virtual

        # Verificar si el entorno virtual existe
        if not os.path.exists(env_path):
            print(f"El entorno virtual '{env_name}' no existe en '{env_path}'.")
            input("Presione Enter para salir...")
            return

        # Iniciar el servidor Django en un hilo separado
        server_thread = threading.Thread(target=run_django_server, args=(env_path,), daemon=True)
        server_thread.start()

        # Esperar a que el servidor se inicie
        time.sleep(2)
        lanzar_navegador()

        # Mantener el script en ejecución mientras el servidor está activo
        while server_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCerrando el servidor...")
    except Exception as ex:
        print(f"Error inesperado en la ejecución: {ex}")
    finally:
        input("Presione Enter para salir...")

if __name__ == "__main__":
    main()
