import sys
import json
import socket
import threading
import time
import struct
import hashlib
import random

class HiloJuego(threading.Thread):

    def __init__(self):
        super().__init__()
        self.identificadorProtocolo = 'DOMINOCOMUNICACIONESI'
        self.mesas = []
        self.inicializar()

    def run(self):
        tiempoInicio = time.time()
        while True:
            try:
                mesa = self.seleccionarMesa(tiempoInicio)
                if mesa:

            finally:
                self.sockUDP.colse()

    def seleccionarMesas(self, tiempoInicio):
        while True:
            mensaje, address = self.sockUDP.recvfrom(4096)
            mensaje_json = json.loads(mensaje.decode('utf-8'))
            if mensaje_json.get('identificador') == self.identificadorProtocolo and 'nombre_mesa' in mensaje_json:
                self.mesas.append({'nombre':mensaje_json['nombre_mesa'],'direccion':address})
                if (time.time() - tiempoInicio) > 20 and len(self.mesas) > 1:
                    while True:
                        print('Mesas disponibles')
                        for i, mesa in enumerate(self.mesas):
                            print('Mesa: {0} Nombre de la mesa {1}',format((i+1),mesa['nombre']))
                        opcion = int(input('Selecciona una mesa por el numero'))
                        if opcion > 0 and opcion <= len(self.mesas):
                            return opcion
                        else:
                            print('Opcion incorrecta, vuelva a intentarlo')

    def inicializar(self):
        UDPendpoint = ('0.0.0.0',3001)
        self.sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)