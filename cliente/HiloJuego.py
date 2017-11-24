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
        input('dale enter para iniciar')
        self.identificadorProtocolo = 'DOMINOCOMUNICACIONESI'
        self.miIdentificador = ''
        self.address_server = None
        self.ronda = 0
        self.mesas = []
        self.fichas = []
        self.jugadores = []
        self.tablero = []
        self.iniciarUDP()

    def run(self):
        tiempoInicio = time.time()
        try:
            mesa = self.seleccionarMesa(tiempoInicio)
            self.cerrarUDP()
            self.nombre = input('ingresa tu nombre de jugador: ')
            self.iniciarTCP(mesa-1)
            print('se desea conectar a: '.format(self.TCPendpoint))
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
                terminoPartida = False
                while not terminoPartida:
                    mensaje_json, address = self.escucharMulticast()
                    print('***********  Mensaje entrante  ***********')
                    print('Se envia desde {}'.format(address))
                    print(mensaje_json)
                    if self.address_server == address and mensaje_json.get('identificador') == self.identificadorProtocolo and 'tipo' in mensaje_json:
                        if mensaje_json['tipo'] == 0 and 'jugadores' in mensaje_json:
                            mensaje_inicio = mensaje_json
                            self.guardarJugadores(mensaje_inicio['jugadores'])
                        elif mensaje_json['tipo'] == 1 and 'ronda' in mensaje_json:
                            mensaje_ronda = mensaje_json
                            self.setRonda(mensaje_ronda['ronda'])
                            print('esperando fichas')
                            mensaje_json = self.escucharTCP()
                            print('mensaje TCP')
                            print(mensaje_json)
                            if mensaje_json['tipo'] == 3 and 'fichas' in mensaje_json:
                                mensaje_fichas = mensaje_json
                                self.guardarFichas(mensaje_fichas['fichas'])
                            terminoRonda = False
                            while not terminoRonda:
                                mensaje_json, address = self.escucharMulticast()
                                print('***********  Mensaje entrante ronda  ***********')
                                print('Se envia desde {}'.format(address))
                                print(mensaje_json)
                                if mensaje_json.get('identificador') == self.identificadorProtocolo and 'jugador' in mensaje_json and 'tipo' in mensaje_json:
                                    # *********************************  YO  **************************************
                                    if mensaje_json['jugador'] == self.miIdentificador:
                                        if mensaje_json['tipo'] == 3 and 'punta_uno' in mensaje_json and 'punta_dos' in mensaje_json:       
                                            if mensaje_json['punta_uno'] == -1 and mensaje_json['punta_dos'] == -1:
                                                ficha, punta = self.jugar(-1,-1, None)
                                            elif 'evento_pasado' in mensaje_json:
                                                evento_pasado = mensaje_json['evento_pasado']
                                                if 'tipo' in evento_pasado and 'jugador' in evento_pasado and 'punta' in evento_pasado:
                                                    if evento_pasado['tipo'] == 0 and 'ficha' in evento_pasado:
                                                        fichaJugada = evento_pasado['ficha']
                                                        if 'entero_uno' in fichaJugada and 'entero_dos' in fichaJugada:
                                                            self.guardarJugada(fichaJugada['entero_uno'], fichaJugada['entero_dos'],evento_pasado['punta'])
                                                            ficha, punta = self.jugar(mensaje_json['punta_uno'], mensaje_json['punta_dos'], mensaje_json['evento_pasado'])             
                                            mensaje_json = {
                                                'identificador': self.identificadorProtocolo,
                                                'ficha': {
                                                    'token': ficha.token
                                                },
                                                'punta': punta
                                            }
                                            self.enviarTCP(mensaje_json)
                                        elif mensaje_json['tipo'] == 4:
                                            terminoRonda = True
                                        elif mensaje_json['tipo'] == 5:
                                            terminoPartida = True
                                        elif mensaje_json['tipo'] == 6:
                                            pass
                                    # *******************************  OTRO  ***************************************
                                    else:
                                        if mensaje_json['tipo'] == 3 and 'punta_uno' in mensaje_json and 'punta_dos' in mensaje_json:            
                                            if mensaje_json['punta_uno'] != -1 and mensaje_json['punta_dos'] != -1 and 'evento_pasado' in mensaje_json:
                                                evento_pasado = mensaje_json['evento_pasado']
                                                if 'tipo' in evento_pasado and 'jugador' in evento_pasado and 'punta' in evento_pasado:
                                                    if evento_pasado['tipo'] == 0 and 'ficha' in evento_pasado:
                                                        fichaJugada = evento_pasado['ficha']
                                                        if 'entero_uno' in fichaJugada and 'entero_dos' in fichaJugada:
                                                            self.guardarJugada(fichaJugada['entero_uno'], fichaJugada['entero_dos'],evento_pasado['punta'])
                                        elif mensaje_json['tipo'] == 4:
                                            terminoRonda = True
                                        elif mensaje_json['tipo'] == 5:
                                            terminoPartida = True
                                        elif mensaje_json['tipo'] == 6:
                                            pass

                        
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

    def jugar(self, punta_uno, punta_dos):
        if punta_uno == -1:
            mayor = 0
            sumaMayor = 0
            for ficha in self.fichas:
                if ficha.punta_uno == ficha.punta_dos and ficha.punta_uno > mayor:
                    mayor = ficha.punta_uno
                    f = ficha
                if ficha.punta_uno != ficha.punta_dos and (ficha.punta_uno+ficha.punta_dos) > sumaMayor:
                    sumaMayor = ficha.punta_uno+ficha.punta_dos
                    fi = ficha
            if f:
                return f, False
            else:
                return fi, False
        else:
            sumaMayor = 0
            fichas = self.fichas
            while len(fichas) > 0:
                for ficha in fichas:
                    if (ficha.punta_uno+ficha.punta_dos) > sumaMayor:
                        sumaMayor = ficha.punta_uno+ficha.punta_dos
                        fichaMayor = ficha
                if fichaMayor.punta_uno == self.tablero[0] or fichaMayor.punta_dos == self.tablero[0]:
                    return fichaMayor, True
                if fichaMayor.punta_uno == self.tablero[len(self.tablero)-1] or fichaMayor.punta_dos == self.tablero[len(self.tablero)-1]:
                    return fichaMayor, False
                fichas.remove(fichaMayor)
            return None, None

    def guardarJugada(self,entero_uno,entero_dos,punta):
        if len(self.tablero) == 0:
                self.tablero.extend([entero_uno, entero_dos])
        elif punta:
            if entero_uno == self.tablero[0]:
                self.tablero.insert(0, entero_uno)
                self.tablero.insert(0, entero_dos)
            elif entero_dos == self.tablero[0]:
                self.tablero.insert(0, entero_dos)
                self.tablero.insert(0, entero_uno)
        else:
            if entero_uno == self.tablero[len(self.tablero)-1]:
                self.tablero.append(entero_uno)
                self.tablero.append(entero_dos)
            elif entero_dos == self.tablero[len(self.tablero)-1]:
                self.tablero.append(entero_dos)
                self.tablero.append(entero_uno)
        print('|', end='')
        for i, f in enumerate(self.tablero):
            print('{0}{1}'.format(f, ':' if(i%2)==0 else '|'), end='')
        print('')

    def guardarJugadores(self,j):
        for jugador in j:
            self.jugadores.append(jugador)

    def guardarFichas(self,f):
        for ficha in f:
            self.fichas.append(Ficha(ficha['entero_uno'], ficha['entero_dos'], ficha['token']))

    def setRonda(self,ronda):
        self.ronda = ronda

    def iniciarUDP(self):
        UDPendpoint = ('0.0.0.0',3001)
        self.sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sockUDP.bind(UDPendpoint)

    def cerrarUDP(self):
        self.sockUDP.close()

    def iniciarTCP(self,mesa):
        self.sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.mesas[mesa]['direccion'])
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

    def escucharMulticast(self):
        mensaje, address= self.sockMulticast.recvfrom(4096)
        if not self.address_server:
            self.address_server = address
        return json.loads(mensaje.decode('utf-8')), address

    def cerrarMulticast(self):
        self.sockMulticast.close()