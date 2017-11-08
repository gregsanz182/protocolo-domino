import sys
import json
import socket
import threading
import time

class HiloDisponibilidad(threading.Thread):

    def __init__(self, identificadorProtocolo):
        super().__init__()
        self.identificadorProtocolo = identificadorProtocolo
        self.UDPendpoint = ('0.0.0.0', 3001)
        self.mesaJson = {
            'identificador': 'DOMINOCOMUNICACIONESI',
            'nombre_mesa': 'la que más aplaude'
        }

    def run(self):
        self.inicializar()

        print('Identificandose en {} por el puerto {}'.format(*self.UDPendpoint))

        self.sockUDP.bind(self.UDPendpoint)

        while self.activo:
            try:
                mensaje, direccion = self.sockUDP.recvfrom(4096)
                if mensaje:
                    msg = json.loads(mensaje.decode('utf-8'))
                    if msg.get('identificador') == self.identificadorProtocolo and self.activo:
                        self.mesaJson['sourceIP'] = direccion
                        self.sockUDP.sendto(json.dumps(self.mesaJson).encode('utf-8'), direccion)
            except TimeoutError:
                pass
        
        self.sockUDP.close()

    def inicializar(self):
        self.sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sockUDP.settimeout(5)
        self.sockUDP.setblocking(True)
        self.activo = True
