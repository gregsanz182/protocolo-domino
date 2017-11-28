import sys
import json
import socket
import threading
import time
import struct
import hashlib
import random
from Cliente.Ficha import Ficha

class HiloJuego(threading.Thread):

    def __init__(self, mainWindow, nombre):
        super().__init__()
        self.mainWindow = mainWindow
        self.nombre = nombre
        self.identificadorProtocolo = 'DOMINOCOMUNICACIONESI'
        self.miIdentificador = ''
        self.address_server = None
        self.puntuacion = 0
        self.ronda = 0
        self.mesa = {}
        self.fichas = []
        self.jugadores = []
        self.tablero = []
        self.iniciarUDP()

    def run(self):
        try:
            self.seleccionarMesa()
            self.cerrarUDP()
            self.iniciarTCP()

            #LLamada a entorno gráfico
            self.mainWindow.setLabelMesa.emit(self.mesa['nombre'])

            mensaje_json = {
                'identificador': self.identificadorProtocolo,
                'nombre_jugador': self.nombre
            }
            self.enviarTCP(mensaje_json)
            mensaje_json = self.escucharTCP()
            if mensaje_json.get('identificador') == self.identificadorProtocolo and 'multicast_ip' in mensaje_json and 'jugador' in mensaje_json:

                #llamada a la interfaz gráfica
                self.mainWindow.inicializarJugador.emit(mensaje_json, self.nombre)
                
                self.miIdentificador = mensaje_json['jugador']
                self.iniciarMulticast(mensaje_json['multicast_ip'])
                terminoPartida = False
                self.puntuacion = 0
                while not terminoPartida:
                    mensaje_json, address = self.escucharMulticast()
                    print('=======>', mensaje_json)
                    if mensaje_json.get('identificador') == self.identificadorProtocolo and 'tipo' in mensaje_json:
                        if mensaje_json['tipo'] == 0 and 'jugadores' in mensaje_json:
                            mensaje_inicio = mensaje_json
                            self.guardarJugadores(mensaje_inicio['jugadores'])
                            #llamada a la interfaz gráfica
                            self.mainWindow.inicializarJugadores.emit(mensaje_inicio)
                        elif mensaje_json['tipo'] == 1 and 'ronda' in mensaje_json:
                            mensaje_ronda = mensaje_json
                            self.ronda = mensaje_ronda['ronda']
                            mensaje_json = self.escucharTCP()
                            if mensaje_json['tipo'] == 2 and 'fichas' in mensaje_json:
                                mensaje_fichas = mensaje_json
                                self.guardarFichas(mensaje_fichas['fichas'])
                            terminoRonda = False
                            while not terminoRonda:
                                mensaje_json, address = self.escucharMulticast()
                                print('pasa multicast')
                                print('mensaje entrante: {}'.format(mensaje_json))
                                if mensaje_json.get('identificador') == self.identificadorProtocolo and 'jugador' in mensaje_json and 'tipo' in mensaje_json:
                                    # *********************************  YO  **************************************
                                    if mensaje_json['jugador'] == self.miIdentificador:
                                        print('juego yo')
                                        if mensaje_json['tipo'] == 3 and 'punta_uno' in mensaje_json and 'punta_dos' in mensaje_json:       
                                            if mensaje_json['punta_uno'] == -1 and mensaje_json['punta_dos'] == -1:
                                                ficha, punta = self.jugar(-1,-1, None)
                                            elif 'evento_pasado' in mensaje_json:
                                                evento_pasado = mensaje_json['evento_pasado']
                                                if 'tipo' in evento_pasado and 'jugador' in evento_pasado and 'punta' in evento_pasado:
                                                    if 'ficha' in evento_pasado:
                                                        fichaJugada = evento_pasado['ficha']
                                                        if 'entero_uno' in fichaJugada and 'entero_dos' in fichaJugada:
                                                            print('guarda mio')
                                                            self.guardarJugada(fichaJugada['entero_uno'], fichaJugada['entero_dos'],evento_pasado['punta'])
                                                            ficha, punta = self.jugar(mensaje_json['punta_uno'], mensaje_json['punta_dos'], mensaje_json['evento_pasado'])             
                                            if ficha is None:
                                                mensaje_json = {
                                                    'identificador': self.identificadorProtocolo,
                                                    'ficha': {
                                                        'token': -1
                                                    },
                                                    'punta': False
                                                }
                                            else:
                                                mensaje_json = {
                                                    'identificador': self.identificadorProtocolo,
                                                    'ficha': {
                                                        'token': ficha.token
                                                    },
                                                    'punta': punta
                                                }
                                                self.fichas.remove(ficha)

                                            print(mensaje_json)
                                            self.enviarTCP(mensaje_json)
                                            print('se envia tcp')
                                        elif mensaje_json['tipo'] == 4:
                                            self.ronda = self.ronda + 1
                                            self.puntuacion = self.puntuacion + mensaje_json['puntuacion']
                                            print('...Ronda Finalizada...')
                                            print('YUPIIIIIIIIIIIII GANE LA RONDA')
                                            print('Puntuacion: {!r}'.format(mensaje_json['puntuacion']))
                                            print('Razón: {!r}'.format(mensaje_json['razon']))
                                            print('Siguiente ronda: {!r}'.format(self.ronda))
                                            terminoRonda = True
                                        elif mensaje_json['tipo'] == 5:
                                            print('...Fin de la partida...')
                                            print('YUPIIIIIIIIIIIII GANE LA PARTIDA')
                                            print('Puntuacion: {!r}'.format(mensaje_json['puntuacion']))
                                            print('Puntuación general')
                                            for j in mensaje['puntuacion_general']:
                                                print('Jugador: {!r} puntuación: {!r}'.format(j['jugador'], j['puntuacion']))
                                            print('Razón: {!r}'.format(mensaje_json['razon']))
                                            terminoPartida = True
                                    # *******************************  OTRO  ***************************************
                                    else:
                                        print('juega otro')
                                        if mensaje_json['tipo'] == 3 and 'punta_uno' in mensaje_json and 'punta_dos' in mensaje_json:            
                                            if mensaje_json['punta_uno'] != -1 and mensaje_json['punta_dos'] != -1 and 'evento_pasado' in mensaje_json:
                                                evento_pasado = mensaje_json['evento_pasado']
                                                if 'tipo' in evento_pasado and 'jugador' in evento_pasado and 'punta' in evento_pasado:
                                                    if evento_pasado['tipo'] == 0 and 'ficha' in evento_pasado:
                                                        fichaJugada = evento_pasado['ficha']
                                                        if 'entero_uno' in fichaJugada and 'entero_dos' in fichaJugada:
                                                            print('guarda otro')
                                                            self.guardarJugada(fichaJugada['entero_uno'], fichaJugada['entero_dos'],evento_pasado['punta'])
                                        elif mensaje_json['tipo'] == 4:
                                            self.ronda = self.ronda + 1
                                            print('...Ronda Finalizada...')
                                            print('No ganaste, tal vez la próxima')
                                            print('Ganador: {!r}'.format(mensaje_json['jugador']))
                                            print('Puntuacion: {!r}'.format(mensaje_json['puntuacion']))
                                            print('Razón: {!r}'.format(mensaje_json['razon']))
                                            print('Siguiente ronda: {!r}'.format(self.ronda))
                                            for jugador in self.jugadores:
                                                if jugador['identificador'] == mensaje_json['jugador']:
                                                    jugador['puntuacion'] = mensaje_json['puntuacion']
                                            terminoRonda = True
                                        elif mensaje_json['tipo'] == 5:
                                            print('...Fin de la partida...')
                                            print('Ganador{!r}'.format(mensaje_json['jugador']))
                                            print('Puntuación general')
                                            for j in mensaje['puntuacion_general']:
                                                print('Jugador: {!r} puntuación: {!r}'.format(j['jugador'], j['puntuacion']))
                                            print('Razón: {!r}'.format(mensaje['razon']))
                                            terminoPartida = True
                                        elif mensaje_json['tipo'] == 6:
                                            print('Jugador se desconecto: {!r}'.format(mensaje_json['jugador']))

                        
            else:
                print('Mensaje incorrecto...')
                print(mensaje_json)

        except socket.error:
            print('Mesa fuera de alcance o llena... lo sentimos')
        self.cerrarUDP()

    def seleccionarMesa(self):
        self.banderaBuscarServer = True
        self.mainWindow.abrirServidoresDialog.emit(self.mesaSeleccionada)
        while self.banderaBuscarServer:
            try:
                mensaje, address = self.sockUDP.recvfrom(4096)
                mensaje_json = json.loads(mensaje.decode('utf-8'))
                if mensaje_json.get('identificador') == self.identificadorProtocolo and 'nombre_mesa' in mensaje_json:
                    self.mainWindow.nuevoServidor.emit({'nombre': mensaje_json['nombre_mesa'], 'direccion': address[0]})
            except (socket.timeout, ValueError):
                pass

    def mesaSeleccionada(self, serverInfo):
        print(serverInfo)
        self.banderaBuscarServer = False
        self.mesa = serverInfo

    def jugar(self, punta_uno, punta_dos, evento_pasado):
        f = fi = None
        if punta_uno == -1:
            mayor = 0
            sumaMayor = 0
            for ficha in self.fichas:
                if ficha.entero_uno == ficha.entero_dos and ficha.entero_uno > mayor:
                    mayor = ficha.entero_uno
                    f = ficha
                if ficha.entero_uno != ficha.entero_dos and (ficha.entero_uno+ficha.entero_dos) > sumaMayor:
                    sumaMayor = ficha.entero_uno+ficha.entero_dos
                    fi = ficha
            if f:
                print(f.entero_uno, f.entero_dos)
                return f, False
            else:
                print(fi.entero_uno, fi.entero_dos)
                return fi, False
        else:
            sumaMayor = 0
            fichaMayor = None
            punta =  None
            for ficha in self.fichas:
                suma = ficha.entero_uno+ficha.entero_dos
                if suma >= sumaMayor:
                    if self.tablero[0] in [ficha.entero_dos, ficha.entero_uno]:
                        fichaMayor = ficha
                        punta = True
                        sumaMayor = suma
                    elif self.tablero[len(self.tablero)-1] in [ficha.entero_dos, ficha.entero_uno]:
                        fichaMayor = ficha
                        punta = False
                        sumaMayor = suma
            return fichaMayor, punta

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
        self.tablero = []
        self.fichas = []
        print('guardando fichas')
        for ficha in f:
            print(ficha['entero_uno'], ficha['entero_dos'])
            self.fichas.append(Ficha(ficha['entero_uno'], ficha['entero_dos'], ficha['token']))

    def iniciarUDP(self):
        UDPendpoint = ('0.0.0.0', 3001)
        self.sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sockUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockUDP.setblocking(1)
        self.sockUDP.settimeout(1)
        self.sockUDP.bind(UDPendpoint)

    def cerrarUDP(self):
        self.sockUDP.close()

    def iniciarTCP(self):
        self.sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.mesa['direccion'])
        self.TCPendpoint = (self.mesa['direccion'], 3001)        
        self.sockTCP.connect(self.TCPendpoint)

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

    def escucharMulticast(self):
        mensaje, address= self.sockMulticast.recvfrom(4096)
        return json.loads(mensaje.decode('utf-8')), address

    def cerrarMulticast(self):
        self.sockMulticast.close()

    def cerrarTodo(self):
        try:
            self.sockUDP.close()
        except:
            pass
        try:
            self.sockTCP.close()
        except:
            pass
        try:
            self.sockMulticast.close()
        except:
            pass