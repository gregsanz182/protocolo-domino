import sys
import json
import socket
import threading
import time

class HiloDisponibilidad(threading.Thread):

    def __init__(self, nombreMesa, identificadorProtocolo):
        super().__init__()
        self.identificadorProtocolo = identificadorProtocolo
        self.UDPendpoint = ('255.255.255.255', 3001)
        self.mesaJson = {
            'identificador': 'DOMINOCOMUNICACIONESI',
            'nombre_mesa': nombreMesa
        }

    def run(self):
        self.inicializar()

        print('Identificandose en {} por el puerto {}'.format(*self.UDPendpoint))

        while self.activo:
            try:
                self.sockUDP.sendto(json.dumps(self.mesaJson).encode('utf-8'), self.UDPendpoint)
                time.sleep(5);
            except socket.error:
                pass
        
        self.sockUDP.close()

    def inicializar(self):
        self.sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.activo = True
