from PyInstaller.utils.hooks import copy_metadata
import argparse
import subprocess
import threading  # Para manejar hilos
import webbrowser  # Para abrir el navegador automáticamente

datas = copy_metadata("django")

def info():
    """
    script para correr la aplicacion py manage.py runserver
    """

def run_django_server():
    """
    Ejecuta el servidor Django en un hilo independiente.
    """
    subprocess.run(['python', 'manage.py', 'runserver'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
    import time
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
