import sys
import json
import socket
import threading
import time
import struct
import hashlib
import random
from Jugador import Jugador
from HiloDisponibilidad import HiloDisponibilidad
from Fichas import Fichas

class HiloJuego(threading.Thread):

    def __init__(self):
        super().__init__()
        self.identificadorProtocolo = 'DOMINOCOMUNICACIONESI'
        self.TCPendpoint = ('0.0.0.0', 3001)
        self.sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.multicastendpoint = ('225.145.80.15', 3001)
        self.sockMulticast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockMulticast.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack('b', 1))
        self.jsonMulticast = {
            'identificador': self.identificadorProtocolo,
            'multicast_ip': self.multicastendpoint[0]
        }
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
        while (time.time() - tiempo_comienzo) < 10 and len(self.jugadores) < 4:
            try:
                conexion, direccion_cliente = self.sockTCP.accept()
                if conexion:
                    conexion.settimeout(5)
                    mensaje = conexion.recv(4096)
                    print('{0} intenta conectarse'.format(direccion_cliente))
                    mensaje_json = json.loads(mensaje.decode('utf-8'))
                    print(mensaje_json)
                    if mensaje_json.get('identificador') == self.identificadorProtocolo and mensaje_json.get('nombre_jugador'):
                        idenJugador = hashlib.md5(str(random.randrange(0, 3500)).encode('utf-8')).hexdigest()
                        respJson = self.jsonMulticast
                        respJson['jugador'] = idenJugador
                        conexion.sendall(json.dumps(self.jsonMulticast).encode('utf-8'))
                        print("El jugador {0} se ha conectado bajo la direccion {1}".format(mensaje_json['nombre_jugador'], direccion_cliente))
                        self.jugadores.append(Jugador(mensaje_json['nombre_jugador'], idenJugador, direccion_cliente, conexion))
                        tiempo_comienzo = time.time()
                        if len(self.jugadores) == 1:
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
        self.repartirFichasYEnviar()
        jugadorTurno = self.jugadorInicial()
        mensajeJuego = {
            'identificador': self.identificadorProtocolo,
            'jugador': jugadorTurno.idenJugador,
            'tipo': 0,
            'punta_uno': -1,
            'punta_dos': -1
        }
        self.enviarBroadcast(mensajeJuego)

            
    def repartirFichasYEnviar(self):
        self.fichasRonda = Fichas(1, [jugador.nombre for jugador in self.jugadores])
        for jugador in self.jugadores:
            jugador.fichas = self.fichasRonda.tomarMano()
        for jugador in self.jugadores:
            jugador.enviarFicha(self.identificadorProtocolo)

    def jugadorInicial(self):
        player = None
        fichaPrior = -1
        for jugador in self.jugadores:
            for ficha in jugador.fichas:
                if ficha['entero_uno'] == ficha['entero_dos'] and ficha['entero_uno'] > fichaPrior:
                    fichaPrior = ficha['entero_uno']
                    player = jugador
        
        if jugador is None:
            for jugador in self.jugadores:
                for ficha in jugador.fichas:
                    if (ficha['entero_uno'] + ficha['entero_dos']) > fichaPrior:
                        fichaPrior = ficha['entero_uno'] + ficha['entero_dos']
                        player = jugador

        return jugador

    def enviarBroadcast(self, data):
        self.sockMulticast.sendto(json.dumps(data).encode('utf-8'), self.multicastendpoint)
