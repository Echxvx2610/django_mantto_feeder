from PyInstaller.utils.hooks import copy_metadata
import subprocess
import threading
import webbrowser
import os
import time

datas = copy_metadata("django")

def run_django_server():
    try:
        env_name = "C:\\envs\\env_django"
        if os.name == 'nt':  # Windows
            activate_script = os.path.join(env_name, 'Scripts', 'activate.bat')
            command = f'call {activate_script} && python manage.py runserver'
        else:
            activate_script = os.path.join(env_name, 'bin', 'activate')
            command = f'source {activate_script} && python manage.py runserver'
        
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el servidor Django: {e}")
    except Exception as ex:
        print(f"Error inesperado: {ex}")
    finally:
        input("Presione Enter para salir...")


def lanzar_navegador():
    url = "http://127.0.0.1:8000"
    webbrowser.open(url)

def main():
    try:
        server_thread = threading.Thread(target=run_django_server, daemon=True)
        server_thread.start()
        time.sleep(2)  # Esperar a que el servidor se inicie
        lanzar_navegador()
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
