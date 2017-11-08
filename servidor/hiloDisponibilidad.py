import sys
import json
import socket
import threading
import time

class hiloDisponibilidad(threading.Thread):

    def __init__(self):
        super().__init__()
        self.UDPendpoint = ('0.0.0.0', 3001)
        self.mesaJson = {
            'identificador': 'DOMINOCOMUNICACIONESI',
            'nombre_mesa': 'la que más aplaude'
        }
        self.sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def run(self):
        print('Escuchando en {} por el puerto {}'.format(*self.UDPendpoint))

        self.sockUDP.bind(self.UDPendpoint)

        while True:
            mensaje, direccion = self.sockUDP.recvfrom(4096)
            if mensaje:
                print("Recibido desde {} por el puerto {}", *direccion)
                msg = json.loads(mensaje.decode('utf-8'))
                print(msg)
                if msg['identificador'] == 'DOMINOCOMUNICACIONESI':
                    self.mesaJson['sourceIP'] = direccion
                    self.sockUDP.sendto(json.dumps(self.mesaJson).encode('utf-8'), direccion)


