#
#   Cliente - Dominó
#

import socket
import json
import sys
import threading
import time

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
        self.sock.close()

    def getMesas(self):
        return self.mesas

    def getIP_Server(self):
        return self.ip_server

class Cliente(threading.Thread):

    def __init__(self,ip):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fichas = []
        self.ip = ip
        try:
            self.sock.connect(self.ip)
            print('conexion exitosa con {} por el puerto {}'.format(*self.ip))
            self.er = False
        except socket.error:
            print('No se pudo realizar la conexión...')
            self.er = True
            sock.close()

    def getError(self):
        return self.er

    def run(self):
        mensaje_TCP = {
            "identificador": "DOMINOCOMUNICACIONESI",
            "nombre_jugador": "Anny Chacón"
        }
        print(mensaje_TCP)
        msj = json.dumps(mensaje_TCP).encode('utf-8')
        self.sock.sendall(msj)
        print('enviado')
        print('esperando multicast...')
        resp = self.sock.recv(4096)
        print(resp)
        respuesta = json.loads(resp.decode('utf-8'))
        if respuesta.get('identificador') == 'DOMINOCOMUNICACIONESI' and respuesta.get('multicast_ip'):
            self.ipMultiCast = respuesta['multicast_ip']
        else:
            print('no se recibio nada')
            self.sock.close()
        fi = self.sock.recv(4096)
        fic = json.loads(fi.decode('utf-8'))
        if fic.get('identificador') == 'DOMINOCOMUNICACIONESI' and fic.get('fichas'):
            for f in fic['fichas']:
                self.fichas.append(f)
                print(f)
        input('terminar: ')
        self.sock.close()


#--------------------------------------------MAIN-------------------------------------------------
if __name__ == '__main__':
    conection = ('255.255.255.255', 3001)
    try:
        lock = threading.Lock()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.setblocking(1)
        sock.settimeout(10)
        req = RequestServer(conection, sock, lock)
        req.start()
        time.sleep(2)
        rep = ReplyServer(sock, lock)
        rep.start()
        req.join()
        rep.join()
        IPs = rep.getIP_Server()
        er = True
        while er == True:
            for i, m in enumerate(rep.getMesas()):
                print(i, m)
            opc = int(input('seleccionar mesa: Ejemplo: [0]: '))
            print(IPs[opc])
            cli = Cliente(IPs[opc])
            er = cli.getError()
        cli.start()

    except socket.error:
        print('error en el socket...')
        sys.exit()
