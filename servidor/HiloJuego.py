import sys
import json
import socket
import threading
import time
from Jugador import Jugador

class HiloJuego(threading.Thread):

    def __init__(self):
        super().__init__()
        self.TCPendpoint = ('localhost', 3001)
        self.jsonMulticast = {
            'identificador': 'DOMINOCOMUNICACIONESI',
            'multicast_ip': '254.569.122'
        }
        self.sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.jugadores = []

    def run(self):
        self.sockTCP.bind(self.TCPendpoint)
        self.sockTCP.listen(1)
        self.sockTCP.settimeout(5)
        self.sockTCP.setblocking(True)
        tiempo_comienzo = time.time()

        while (tiempo_comienzo - time.time()) < 30 :
            try:
                conexion, direccion_cliente = self.sockTCP.accept()
                if conexion:
                    conexion.settimeout(5)
                    mensaje = conexion.recv(4096)
                    mensaje_json = json.loads(mensaje.decode('utf-8'))
                    if mensaje_json['indentificador'] == 'DOMINOCOMUNICACIONESI' and mensaje_json.get('nombre_jugador'):
                        self.jugadores.append(new Jugador(mensaje_json['nombre_jugador'], direccion_cliente, conexion))
            except TimeoutError:
                pass
                
            if len(self.jugadores) < 4:
                tiempo_comienzo = time.time()
    
