import sys
import json
import socket
import threading
import time
import struct
import hashlib
import random
from Servidor.Jugador import Jugador
from Servidor.HiloDisponibilidad import HiloDisponibilidad
from Servidor.Fichas import Fichas

class HiloJuego(threading.Thread):

    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.identificadorProtocolo = 'DOMINOCOMUNICACIONESI'
        self.TCPendpoint = ('0.0.0.0', 3001)
        self.sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
        self.iniciarjuego()

    def lobby(self):
        self.enviarUDP()
        self.sockTCP.bind(self.TCPendpoint)
        self.sockTCP.listen(4)
        self.sockTCP.setblocking(1)
        tiempo_comienzo = time.time()
        countdown = False
        while (time.time() - tiempo_comienzo) < 10 and len(self.jugadores) < 4:
            try:
                print('esperando conexiones de los clientes')
                conexion, direccion_cliente = self.sockTCP.accept()
                print('pasa')
                if conexion:
                    self.sockTCP.settimeout(5)
                    mensaje = conexion.recv(4096)
                    print('{0} intenta conectarse'.format(direccion_cliente))
                    mensaje_json = json.loads(mensaje.decode('utf-8'))
                    if mensaje_json.get('identificador') == self.identificadorProtocolo and 'nombre_jugador' in mensaje_json:
                        idenJugador = hashlib.md5(str(random.randrange(0, 3500)).encode('utf-8')).hexdigest()
                        respJson = self.jsonMulticast
                        respJson['jugador'] = idenJugador
                        conexion.sendall(json.dumps(self.jsonMulticast).encode('utf-8'))
                        print("El jugador {0} se ha conectado bajo la direccion {1}".format(mensaje_json['nombre_jugador'], direccion_cliente))
                        self.jugadores.append(Jugador(mensaje_json['nombre_jugador'], idenJugador, direccion_cliente, conexion))

                        #llamada a interfaz gráfica
                        self.mainWindow.inicializarJugador.emit(respJson, mensaje_json['nombre_jugador'])

                        tiempo_comienzo = time.time()
                        if len(self.jugadores) == 1:
                            countdown = True
            except (socket.timeout, ValueError):
                pass
                
            if countdown == False:
                tiempo_comienzo = time.time()
        
        self.detenerUDP()
    
    def enviarUDP(self):
        self.disp.start()

    def detenerUDP(self):
        self.disp.activo = False

    def iniciarjuego(self):
        print("Iniciando Partida")
        self.ronda = 1;
        mensajeJuego = {
            'identificador': self.identificadorProtocolo,
            'tipo': 0,
            'jugadores': []
        }
        for jugador in self.jugadores:
            mensajeJuego['jugadores'].append({'identificador':jugador.idenJugador,'nombre':jugador.nombre})
        self.enviarMulticast(mensajeJuego)
        time.sleep(1)
        contadorPuntos = 0
        while contadorPuntos < 100:
            print("Iniciando Ronda #{}".format(self.ronda))
            mensajeJuego = {
                'identificador': self.identificadorProtocolo,
                'tipo': 1,
                'ronda': self.ronda
            }
            self.enviarMulticast(mensajeJuego)

            #llamada a interfaz gráfica
            self.mainWindow.cambiarRonda.emit(mensajeJuego)
            
            time.sleep(2)
            self.repartirFichasYEnviar()
            time.sleep(2)
            jugadorTurno = self.jugadorInicial()
            mensajeJuego = {
                'identificador': self.identificadorProtocolo,
                'jugador': jugadorTurno.idenJugador,
                'tipo': 3,
                'punta_uno': -1,
                'punta_dos': -1
            }
            tableroCola = []
            jugando = True
            self.enviarMulticast(mensajeJuego)
            self.mainWindow.procesarJugada.emit(mensajeJuego)
            time.sleep(2)
            while jugando:
                evento_pasado = self.esperarYrealizarJugada(jugadorTurno, tableroCola)
                time.sleep(2)
                jugadorGanador, razon = self.validarFinRonda(tableroCola, jugadorTurno)
                if jugadorGanador:
                    mensajeJuego = {
                        'identificador': self.identificadorProtocolo,
                        'jugador': jugadorGanador.idenJugador,
                        'tipo': 4,
                        'puntuacion': self.calcularPuntuacion(jugadorGanador),
                        'razon': razon
                    }
                    contadorPuntos += self.calcularPuntuacion(jugadorGanador)
                    jugando = False
                else:
                    jugadorTurno = self.jugadores[(self.jugadores.index(jugadorTurno)+1)%len(self.jugadores)]
                    mensajeJuego = {
                        'identificador': self.identificadorProtocolo,
                        'jugador': jugadorTurno.idenJugador,
                        'tipo': 3,
                        'punta_uno': tableroCola[0],
                        'punta_dos': tableroCola[len(tableroCola)-1],
                        'evento_pasado': evento_pasado
                    }
                print('|', end='')
                for i, ficha in enumerate(tableroCola):
                    print('{0}{1}'.format(ficha, ':' if (i%2)==0 else '|'), end='')
                print('')
                if mensajeJuego['tipo'] == 1:
                    print(mensajeJuego)
                self.mainWindow.procesarJugada.emit(mensajeJuego)
                self.enviarMulticast(mensajeJuego)
        mensajeJuego = {
            'identificador': self.identificadorProtocolo,
            'jugador': jugadorGanador.idenJugador,
            'tipo': 4,
            'puntuacion': self.calcularPuntuacion(jugadorGanador),
            'razon': razon
        }
            
    def repartirFichasYEnviar(self):
        self.fichasRonda = Fichas(1, [jugador.nombre for jugador in self.jugadores])
        for jugador in self.jugadores:
            jugador.fichas = self.fichasRonda.repartirFichas()
        for jugador in self.jugadores:
            men = jugador.enviarFicha(self.identificadorProtocolo)
            #llamada a interfaz gráfica
            self.mainWindow.ponerManoJugador.emit(men, jugador.idenJugador)

    def jugadorInicial(self):
        player = None
        fichaPrior = -1
        for jugador in self.jugadores:
            for ficha in jugador.fichas:
                if ficha['entero_uno'] == ficha['entero_dos'] and (ficha['entero_uno'] + ficha['entero_dos']) > fichaPrior:
                    fichaPrior = ficha['entero_uno']
                    player = jugador
        
        if player is None:
            for jugador in self.jugadores:
                for ficha in jugador.fichas:
                    if (ficha['entero_uno'] + ficha['entero_dos']) > fichaPrior:
                        fichaPrior = ficha['entero_uno'] + ficha['entero_dos']
                        player = jugador

        return player

    def enviarMulticast(self, data):
        print(data)
        self.sockMulticast.sendto(json.dumps(data).encode('utf-8'), self.multicastendpoint)

    def esperarYrealizarJugada(self, jugador, tableroCola):
        evento_pasado = {}
        mensaje = jugador.socketTCP.recv(4096)
        menJson = json.loads(mensaje.decode('utf-8'))
        if menJson.get('identificador') == self.identificadorProtocolo and 'ficha' in menJson and 'token' in menJson['ficha']:
            if menJson['ficha']['token'] == -1:
                return {
                    'tipo': 2,
                    'jugador': jugador.idenJugador
                }
            ficha = jugador.verificarFicha(menJson['ficha']['token'])
            if ficha:
                evento_pasado = {
                    'jugador': jugador.idenJugador,
                    'ficha': {
                        'entero_uno': ficha['entero_uno'],
                        'entero_dos': ficha['entero_dos']
                    },
                    'punta': menJson['punta']
                }
                if self.realizarJugada(tableroCola, ficha, menJson['punta']):
                    jugador.fichas.remove(ficha)
                    evento_pasado['tipo'] = 0
                else:
                    evento_pasado['tipo'] = 1
            else:
                evento_pasado['tipo'] = 1
            return evento_pasado


    def realizarJugada(self, tableroCola, ficha, punta):
        if len(tableroCola) == 0:
                tableroCola.extend([ficha['entero_uno'], ficha['entero_dos']])
                return True
        elif punta:
            if ficha['entero_dos'] == tableroCola[0]:
                tableroCola.insert(0, ficha['entero_dos'])
                tableroCola.insert(0, ficha['entero_uno'])
                return True
            elif ficha['entero_uno'] == tableroCola[0]:
                tableroCola.insert(0, ficha['entero_uno'])
                tableroCola.insert(0, ficha['entero_dos'])
                return True
        else:
            if ficha['entero_uno'] == tableroCola[len(tableroCola)-1]:
                tableroCola.append(ficha['entero_uno'])
                tableroCola.append(ficha['entero_dos'])
                return True
            elif ficha['entero_dos'] == tableroCola[len(tableroCola)-1]:
                tableroCola.append(ficha['entero_dos'])
                tableroCola.append(ficha['entero_uno'])
                return True
        return False

    def validarFinRonda(self, tableroCola, jugador):
        #Dominó ronda
        if len(jugador.fichas) == 0:
            return jugador, "Dominó la ronda"
        
        #Tranca
        if self.validarTranca(tableroCola):
            cantidades = [player.contarPintas() for player in self.jugadores]
            minimo = min(cantidades)

            #El jugador con menor pintas
            if cantidades.count(minimo) == 1:
                return self.jugadores[cantidades.index(minimo)], "Menor cantidad de pintas"
            else:
                #El que trancó
                if jugador.contarPintas() == minimo:
                    return jugador, "Menor cantidad de pintas y que trancó"
                else:
                    c = 1
                    while True:
                        jugadorSiguiente = self.jugadores[(self.jugadores.index(jugador)+c)%len(self.jugadores)]
                        if jugadorSiguiente.contarPintas() == minimo:
                            return jugadorSiguiente, "Menor cantidad de pintas prox. al que trancó"

        return None, None

    def validarTranca(self, tableroCola):
        if len(tableroCola) == 0:
            return False
        for jugador in self.jugadores:
            if jugador.disponibilidadPinta(tableroCola[0]) or jugador.disponibilidadPinta(tableroCola[len(tableroCola)-1]):
                return False
        return True
    
    def calcularPuntuacion(self, jugador):
        suma = 0
        for player in self.jugadores:
            if player != jugador:
                suma += player.contarPintas()
        
        return suma

    def cerrarTodo(self):
        if self.disp.is_alive:
            self.disp.activo = False
        try:
            self.sockTCP.close()
        except:
            pass
