from PyInstaller.utils.hooks import copy_metadata
import argparse
import subprocess
import threading  # Para manejar hilos
import webbrowser  # Para abrir el navegador automáticamente
import os
import time

datas = copy_metadata("django")

def info():
    """
    script para correr la aplicacion py manage.py runserver
    """

def run_django_server():
    """
    Ejecuta el servidor Django en un hilo independiente dentro del entorno virtual.
    """
    # Ruta del entorno virtual
    env_name = "env_django"
    
    if os.name == 'nt':  # Windows
        # En Windows activamos el entorno virtual con 'Activate.bat'
        activate_script = os.path.join(env_name, 'Scripts', 'activate.bat')
        command = f'call {activate_script} && python manage.py runserver'
    else:  # Unix/MacOS
        # En Linux/Mac activamos con 'source'
        activate_script = os.path.join(env_name, 'bin', 'activate')
        command = f'source {activate_script} && python manage.py runserver'
    
    # Ejecutar el comando de activación y el servidor Django en el subproceso
    subprocess.run(command, shell=True)

def lanzar_navegador():
    """
    Abre el navegador en la dirección del servidor.
    """
    url = "http://127.0.0.1:8000"
    webbrowser.open(url)

def main():
    parser = argparse.ArgumentParser(description='Iniciar un servidor web y cargar una página HTML.')
    args = parser.parse_args()
    
    # Crear y lanzar el hilo para el servidor Django
    server_thread = threading.Thread(target=run_django_server, daemon=True)
    server_thread.start()
    
    # Esperar un breve momento para asegurarse de que el servidor está corriendo
    time.sleep(2)
    
    # Abrir el navegador
    lanzar_navegador()
    
    # Mantener el script principal activo mientras el servidor está corriendo
    try:
        while server_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCerrando el servidor...")

if __name__ == "__main__":
    main()
