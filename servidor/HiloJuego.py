import sys
import json
import socket
import threading
import time
from Jugador import Jugador
from HiloDisponibilidad import HiloDisponibilidad

class HiloJuego(threading.Thread):

    def __init__(self):
        super().__init__()
        self.identificadorProtocolo = 'DOMINOCOMUNICACIONESI'
        self.TCPendpoint = ('localhost', 3001)
        self.jsonMulticast = {
            'identificador': self.identificadorProtocolo,
            'multicast_ip': '254.569.122'
        }
        self.sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.jugadores = []
        self.disp = HiloDisponibilidad(self.identificadorProtocolo)

    def run(self):
        self.lobby()

    def lobby(self):
        self.escucharUDP()
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
                    if mensaje_json['indentificador'] == self.identificadorProtocolo and mensaje_json.get('nombre_jugador'):
                        self.jugadores.append(Jugador(mensaje_json['nombre_jugador'], direccion_cliente, conexion))
            except TimeoutError:
                pass
                
            if len(self.jugadores) < 2:
                tiempo_comienzo = time.time()
        
        self.detenerUDP()
    
    def escucharUDP(self):
        self.disp.start()

    def detenerUDP(self):
        self.disp.activo = False