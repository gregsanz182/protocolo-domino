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
        self.iniciarUDP()

    def run(self):
        tiempoInicio = time.time()
        try:
            while True:
                mesa = self.seleccionarMesa(tiempoInicio)
                if mesa == -1:
                    break
                self.nombre = input('ingresa tu nombre de jugador: ')
                self.iniciarTCP(mesa-1)
                self.TCPendpoint = (self.mesas[mesa-1]['direccion'],3001)
                self.sockTCP.connect(self.TCPendpoint)
                print('Conexion exitosa')
                mensaje_json = {
                    'identificador': self.identificadorProtocolo,
                    'nombre_jugador': self.nombre
                }
                self.enviarTCP(mensaje_json)
                print('envio de TCP exitoso hasta aqui llega cliente')

        except socket.error:
            print('Mesa fuera de alcanse o llena... lo sentimos')
        self.sockUDP.close()

    def seleccionarMesa(self, tiempoInicio):
        while True:
            mensaje, address = self.sockUDP.recvfrom(4096)
            mensaje_json = json.loads(mensaje.decode('utf-8'))
            if mensaje_json.get('identificador') == self.identificadorProtocolo and 'nombre_mesa' in mensaje_json:
                band = True
                for mesa in self.mesas:
                    print(mesa)
                    if mesa.get('nombre') == mensaje_json['nombre_mesa']:
                        band = False
                if band:
                    self.mesas.append({'nombre':mensaje_json['nombre_mesa'],'direccion':address[0]})
            if (time.time() - tiempoInicio) > 2 and len(self.mesas) > 0:
                while True:
                    print('Mesas disponibles')
                    for i, mesa in enumerate(self.mesas):
                        print('Mesa: {0} Nombre de la mesa: {1}'.format((i+1),mesa['nombre']))
                    opcion = int(input('Selecciona una mesa por el numero:'))
                    if opcion > 0 and opcion <= len(self.mesas):
                        return opcion
                    else:
                        print('Opcion incorrecta, vuelva a intentarlo')
            if (time.time() - tiempoInicio) > 20 and len(self.mesas) == 0:
                print('tiempo agotado en espera de mesas...')
                return -1

    def iniciarUDP(self):
        UDPendpoint = ('0.0.0.0',3001)
        self.sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sockUDP.bind(UDPendpoint)

    def iniciarTCP(self,mesa):
        self.sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def enviarTCP(self,mensaje):
        self.sockTCP.sendall(json.dumps(mensaje).encode('utf-8'))