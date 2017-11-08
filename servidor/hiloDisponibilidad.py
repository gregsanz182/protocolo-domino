import sys
import json
import socket
import threading

class hiloDisponibilidad(threading.Thread):

    def __init__(self):
        self.endpoint = ('0.0.0.0', 3001)
        self.mesaJson = {
            'identificador': 'DOMINOCOMUNICACIONESI',
            'nombre_mesa': 'la que más aplaude'
        }
        self.sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        print('Escuchando en {} por el puerto {}'.format(*self.endpoint))

        self.sockUDP.bind(self.endpoint)

        while True:
            mensaje, direccion = self.sockUDP.recvfrom(4096)

            if mensaje:
                msg = json.loads(mensaje.decode('utf-8'))
                if msg['identificador'] == 'DOMINOCOMUNICACIONESI':
                    self.sockUDP.sendto(json.dumps(self.mesaJson).encode('utf-8'), direccion)


