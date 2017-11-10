#
#   Cliente - Dominó
#

import socket
import json
import sys
import threading
import time
import struct

#----------------------------------------REQUEST----------------------------------------------------
class RequestServer(threading.Thread):

    def __init__(self, conection, sock, lock):
        super().__init__()
        self.lock = lock
        self.sock = sock
        self.conection = conection
        self.mensaje_json = {
            "identificador": "DOMINOCOMUNICACIONESI"
        }

    def run(self):
        #while True:
        #lock.acquire()
        self.mensaje = json.dumps(self.mensaje_json).encode('utf-8')
        #lock.release()
        self.sock.sendto(self.mensaje, self.conection)
        print('mensaje cliente: {}'.format(self.mensaje))
        time.sleep(2)

#------------------------------------------REPLY--------------------------------------------------
class ReplyServer(threading.Thread):

    def __init__(self, sock, lock):
        super().__init__()
        self.lock = lock
        self.sock = sock
        self.mesas = []
        self.ip_server = []

    def run(self):
        while True:
            try:
                #lock.acquire()
                self.msj, self.direc = self.sock.recvfrom(4096)
                #lock.release()
                self.mensaje = json.loads(self.msj.decode('utf-8'))
                if self.mensaje.get('identificador') == 'DOMINOCOMUNICACIONESI' and self.mensaje.get('nombre_mesa'):
                    self.mesas.append(self.mensaje['nombre_mesa'])
                    self.ip_server.append(self.direc)
                    print(self.mesas)
                    print(self.ip_server)
            except socket.timeout:
                print('no hay mas respuestas de las mesas')
                break

    def getMesas(self):
        return self.mesas

    def getIP_Server(self):
        return self.ip_server

class Cliente(threading.Thread):

    def __init__(self,ip,nombre,mano):
        super().__init__()
        self.sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fichas = []
        self.ip_address = ip
        self.nombre = nombre
        self.mano = mano
        self.puntuacion = 0
        self.jugadores = []
        self.fichas_jugadas = []
        self.jugadas_erroneas = []
        self.jugador_retirado = []
        self.ronda = 1
        self.tablero = []
        try:
            self.sockTCP.connect(self.ip_address)
            print('conexion exitosa con {} por el puerto {}'.format(*self.ip_address))
            self.er = False
        except socket.error:
            print('No se pudo realizar la conexión...')
            self.er = True
            self.sockTCP.close()

    def getError(self):
        return self.er

    def run(self):
        mensaje_TCP = {
            "identificador": "DOMINOCOMUNICACIONESI",
            "nombre_jugador": "Anny Chacón"
        }
        print(mensaje_TCP)
        msj = json.dumps(mensaje_TCP).encode('utf-8')
        self.sockTCP.sendall(msj)
        print('enviado')
        print('esperando multicast...')
        data = self.sockTCP.recv(4096)
        print(data)
        respuesta = json.loads(data.decode('utf-8'))
        if respuesta.get('identificador') == 'DOMINOCOMUNICACIONESI' and respuesta.get('multicast_ip') and respuesta.get('jugador'):
            self.ipMulticast = respuesta['multicast_ip']
            self.identificador_jugador = respuesta['jugador']
            #bind_addr = '0.0.0.0'
            port = self.ip_address[1]
            sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sockUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            sockUDP.bind(('192.168.0.3', port))
            #sockUDP.bind((bind_addr, port))
            #membership = socket.inet_aton(self.ipMulticast) + socket.inet_aton(bind_addr)
            membership = struct.pack("4sl", socket.inet_aton(self.ipMulticast), socket.INADDR_ANY)

            sockUDP.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)

            data = self.sockTCP.recv(4096)
            fic = json.loads(data.decode('utf-8'))
            if fic.get('identificador') == 'DOMINOCOMUNICACIONESI' and fic.get('fichas'):
                for f in fic['fichas']:
                    self.fichas.append(f)
                    print(f)
                self.jugar(sockUDP)
        else:
            print('No hay respuesta del servidor')

        self.sockTCP.close()

    def jugar(self,sockUDP):
        while True:
            #-------------------------------------------------------------MSJ MULTICAST---------------------------------------------------
            data, address = sockUDP.recvfrom(4096)
            mensaje = json.loads(data.decode('utf-8'))
            print('mensaje multicast: {!r}'.format(mensaje))
            if mensaje.get('identificador') == 'DOMINOCOMUNICACIONESI' and mensaje.get('jugador') and 'tipo' in mensaje:
                jugador = mensaje['jugador']
                if jugador == self.identificador_jugador:
                    #-------------------------------------------------------MSJ TIPO 0----------------------------------------------------
                    if mensaje.get('tipo') == 0:
                        if mensaje.get('punta_uno') != -1 and (mensaje.get('punta_dos') != -1 and mensaje.get('evento_pasado')):
                            evento_pasado = mensaje['evento_pasado']
                            #-----------------------------------JUGADA NORMAL--------GUARDANDO PUNTAS-----------------------------------------
                            if evento_pasado.get('tipo') == 0 and evento_pasado.get('jugador') and evento_pasado.get('ficha'):
                                self.guardarJugada(mensaje['punta_uno'], mensaje['punta_dos'])
                                self.fichas_jugadas.append(evento_pasado['ficha'])

                        ficha, punta = self.obtenerJugada(mensaje)
                        if ficha == None:
                            mensaje_TCP = {
                                "identificador": "DOMINOCOMUNICACIONESI",
                                "ficha": {
                                    "token": -1
                                },
                                "punta": False
                            }
                        else:
                            mensaje_TCP = {
                                "identificador": "DOMINOCOMUNICACIONESI",
                                "ficha": {
                                    "token": ficha['token']
                                },
                                "punta": punta
                            }
                            print('token: {!r} punta: {!r} a jugar'.format(ficha['token'], punta))
                            self.fichas.remove(ficha)
                        try:
                            mensaje_envio = json.dumps(mensaje_TCP).encode('utf-8')
                            self.sockTCP.sendall(mensaje_envio)
                        except socket.error:
                            print('error de socket TCP')
                            self.sockTCP.close()
                    elif mensaje.get('tipo') == 1:
                        self.ronda = self.ronda + 1
                        print('...Ronda Finalizada...')
                        print('YUPIIIIIIIIIIIII GANE LA RONDA')
                        print('Puntuacion: {!r}'.format(mensaje['puntuacion']))
                        print('Razón: {!r}'.format(mensaje['razon']))
                        print('Siguiente ronda: {!r}'.format(self.ronda))
                    #-------------------------------------------------------MSJ TIPO 1----------------------------------------------------
                elif mensaje.get('tipo') == 1:
                    self.ronda = self.ronda + 1
                    print('...Ronda Finalizada...')
                    print('No ganaste, tal vez la próxima')
                    print('Jugador Ganador: {!r}'.format(jugador))
                    print('Puntuacion: {!r}'.format(mensaje['puntuacion']))
                    print('Razón: {!r}'.format(mensaje['razon']))
                    print('Siguiente ronda: {!r}'.format(self.ronda))
                else:
                    print('no es mi turno')
            else:
                print('Mensaje erroneo')
        #--------------------------------------------------------------END WHILE----------------------------------------------------------

    def obtenerJugada(self, mensaje):
        if mensaje.get('punta_uno') == -1 and mensaje.get('punta_dos') == -1 and self.ronda == 1:
            self.mano = 'yo'
            x = 6
            suma = []
            aux = 0
            pos = 0
            for i, f in enumerate(self.fichas):
                if f['entero_uno'] == x and f['entero_dos'] == x:
                    return f, False
                x = x - 1
                suma.append(f['entero_uno'] + f['entero_dos'])
                if suma[i] > aux:
                    aux = suma[i]
                    pos = i
            return self.fichas[pos], False
        else:
            if len(self.tablero) == 0:
                return self.fichas[randrange(len(self.fichas))], False
            for f in self.fichas:
                if f['entero_uno'] == self.tablero[0] or f['entero_dos'] == self.tablero[0]:
                    return f, True
                if f['entero_uno'] == self.tablero[len(self.tablero)-1] or f['entero_dos'] == self.tablero[len(self.tablero)-1]:
                    return f, False
            return None, None

    def guardarJugada(self,punta_uno,punta_dos):
        if len(self.tablero) == 0:
            self.tablero.extend([punta_uno, punta_dos])
        else:
            self.tablero.insert(0, punta_uno)
            self.tablero.append(punta_dos)
        
#--------------------------------------------MAIN-------------------------------------------------
if __name__ == '__main__':
    conection = ('255.255.255.255', 3001)
    nombre = 'Anny Chacón'
    try:
        lock = threading.Lock()
        sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sockUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sockUDP.setblocking(1)
        sockUDP.settimeout(10)
        req = RequestServer(conection, sockUDP, lock)
        req.start()
        time.sleep(2)
        rep = ReplyServer(sockUDP, lock)
        rep.start()
        req.join()
        rep.join()
        sockUDP.close()
        IPs = rep.getIP_Server()
        er = True
        if IPs:
            while er == True and IPs:
                for i, m in enumerate(rep.getMesas()):
                    print(i, m)
                opc = int(input('seleccionar mesa: Ejemplo: [0]: '))
                print(IPs[opc])
                cli = Cliente(IPs[opc],nombre,'')
                er = cli.getError()
            cli.start()
        else:
            print('no hay servidores disponibles')

    except socket.error:
        print('error en el socket...')
        sockUDP.close()
        sys.exit()
