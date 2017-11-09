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
                if self.mensaje['identificador'] == 'DOMINOCOMUNICACIONESI':
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

#--------------------------------------------MAIN-------------------------------------------------
if __name__ == '__main__':
    conection = ('127.255.255.255', 3001)
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
        for i, m in enumerate(rep.getMesas()):
            print(i, m)
        opc = int(input('seleccionar mesa: Ejemplo: [1]: '))
    except socket.error:
        print('error en el socket...')
        sys.exit()
