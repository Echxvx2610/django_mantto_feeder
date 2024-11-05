import sys
import os
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
import threading

class SimpleWebServer:
    def __init__(self, port):
        self.port = port
        self.handler = SimpleHTTPRequestHandler

    def start(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Cambiar al directorio del script
        server = HTTPServer(('localhost', self.port), self.handler)
        print(f'Servidor web iniciado en http://127.0.0.1:{self.port}')
        server.serve_forever()

class MainWindow(QMainWindow):
    def __init__(self, port):
        super().__init__()
        self.setWindowTitle("Visualizador de Gráficos")
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.browser.setUrl(f"http://127.0.0.1:{port}/graficos.html")

def run_server(port):
    server = SimpleWebServer(port)
    server.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Iniciar un servidor web y cargar una página HTML.')
    parser.add_argument('--port', type=int, default=5500, help='Puerto del servidor (default: 5500)')
    args = parser.parse_args()

    # Iniciar el servidor en un hilo separado
    server_thread = threading.Thread(target=run_server, args=(args.port,), daemon=True)
    server_thread.start()

    # Iniciar la aplicación PySide6
    app = QApplication(sys.argv)
    window = MainWindow(args.port)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
