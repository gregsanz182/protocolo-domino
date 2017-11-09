import sys
import json
import socket
import threading
import time
from Jugador import Jugador
from HiloDisponibilidad import HiloDisponibilidad
from Fichas import Fichas

class HiloJuego(threading.Thread):

    def __init__(self):
        super().__init__()
        self.identificadorProtocolo = 'DOMINOCOMUNICACIONESI'
        self.TCPendpoint = ('0.0.0.0', 3001)
        self.jsonMulticast = {
            'identificador': self.identificadorProtocolo,
            'multicast_ip': '254.569.122'
        }
        self.sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.jugadores = []
        self.disp = HiloDisponibilidad(self.identificadorProtocolo)

    def run(self):
        self.lobby()
        self.iniciarRonda()

    def lobby(self):
        self.escucharUDP()
        self.sockTCP.bind(self.TCPendpoint)
        self.sockTCP.listen(1)
        self.sockTCP.settimeout(5)
        tiempo_comienzo = time.time()
        countdown = False
        while (time.time() - tiempo_comienzo) < 30 and len(self.jugadores) < 4:
            try:
                conexion, direccion_cliente = self.sockTCP.accept()
                if conexion:
                    conexion.settimeout(5)
                    mensaje = conexion.recv(4096)
                    print('{0} intenta conectarse', direccion_cliente)
                    mensaje_json = json.loads(mensaje.decode('utf-8'))
                    if mensaje_json.get('identificador') == self.identificadorProtocolo and mensaje_json.get('nombre_jugador'):
                        conexion.sendall(json.dumps(self.jsonMulticast).encode('utf-8'))
                        print("El jugador {0} se ha conectado bajo la direccion {1}".format(mensaje_json['nombre_jugador'], direccion_cliente))
                        self.jugadores.append(Jugador(mensaje_json['nombre_jugador'], direccion_cliente, conexion))
                        tiempo_comienzo = time.time()
                        if len(self.jugadores) == 2:
                            countdown = True
            except (socket.timeout, ValueError):
                pass
                
            if countdown == False:
                tiempo_comienzo = time.time()
        
        self.detenerUDP()
    
    def escucharUDP(self):
        self.disp.start()

    def detenerUDP(self):
        self.disp.activo = False

    def iniciarRonda(self):
        print("Iniciando Ronda")
        self.fichasRonda = Fichas(1, [jugador.nombre for jugador in self.jugadores])
        for jugador in self.jugadores:
            jugador.fichas = self.fichasRonda.tomarMano()
            
        self.enviarFichas()

    def enviarFichas(self):
        for jugador in self.jugadores:
            jugador.enviarFicha()

