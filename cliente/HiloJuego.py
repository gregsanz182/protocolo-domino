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
            mesa = self.seleccionarMesa(tiempoInicio)
            self.cerrarUDP()
            self.nombre = input('ingresa tu nombre de jugador: ')
            self.iniciarTCP(mesa-1)
            self.sockTCP.connect(self.TCPendpoint)
            print('Conexion exitosa')
            mensaje_json = {
                'identificador': self.identificadorProtocolo,
                'nombre_jugador': self.nombre
            }
            self.enviarTCP(mensaje_json)
            mensaje_json = self.escucharTCP()
            if mensaje_json.get('identificador') == self.identificadorProtocolo and 'multicast_ip' in mensaje_json and 'jugador' in mensaje_json:
                self.miIdentificador = mensaje_json['jugador']
                self.iniciarMulticast(mensaje_json['multicast_ip'])

                while True:
                    mensaje, address= self.sockMulticast.recvfrom(4096)
                    mensaje_json = json.loads(mensaje.decode('utf-8'))
                    print('ensaje entrante')
                    print(mensaje_json)
                    if mensaje_json.get('identificador') == self.identificadorProtocolo and 'tipo' in mensaje_json and 'jugadores' in mensaje_json:
                        mensaje_inicio = mensaje_json
                    if mensaje_json.get('identificador') == self.identificadorProtocolo and 'tipo' in mensaje_json and 'ronda' in mensaje_json:
                        mensaje_ronda = mensaje_json
                        
            else:
                print('Mensaje incorrecto...')
                print(mensaje_json)

        except socket.error:
            print('Mesa fuera de alcanse o llena... lo sentimos')
        self.cerrarUDP()

    def seleccionarMesa(self, tiempoInicio):
        while True:
            mensaje, address = self.sockUDP.recvfrom(4096)
            mensaje_json = json.loads(mensaje.decode('utf-8'))
            if mensaje_json.get('identificador') == self.identificadorProtocolo and 'nombre_mesa' in mensaje_json:
                band = True
                for mesa in self.mesas:
                    if mesa.get('nombre') == mensaje_json['nombre_mesa']:
                        band = False
                if band:
                    self.mesas.append({'nombre':mensaje_json['nombre_mesa'],'direccion':address[0]})
            if (time.time() - tiempoInicio) > 2 and len(self.mesas) > 0:
                while True:
                    print('Mesas disponibles')
                    for i, mesa in enumerate(self.mesas):
                        print('Mesa: {0} Nombre de la mesa: {1}'.format((i+1),mesa['nombre']))
                    opcion = int(input('Selecciona una mesa por el numero: '))
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

    def cerrarUDP(self):
        self.sockUDP.close()

    def iniciarTCP(self,mesa):
        self.sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCPendpoint = (self.mesas[mesa]['direccion'],3001)        

    def enviarTCP(self,mensaje):
        self.sockTCP.sendall(json.dumps(mensaje).encode('utf-8'))

    def escucharTCP(self):
        mensaje = self.sockTCP.recv(4096)
        return json.loads(mensaje.decode('utf-8'))

    def cerrarTCP(self):
        self.sockTCP.close()

    def iniciarMulticast(self,direccion):
        self.sockMulticast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockMulticast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockMulticast.bind(('0.0.0.0', 3001))
        membership = struct.pack("4sl", socket.inet_aton(direccion), socket.INADDR_ANY)
        self.sockMulticast.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)
        print('conexion multicast exitosa')

    def cerrarMulticast(self):
        self.sockMulticast.close()