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

    def __init__(self, conection, sock):
        super().__init__()
        self.conection = conection
        self.sock = sock
        self.mensaje_json = {
            "identificador": "DOMINOCOMUNICACIONES1"
        }

    def run(self):
        while True:
            self.mensaje = json.dumps(self.mensaje_json).encode('utf-8')
            sock.sendto(self.mensaje, self.conection)
            print('mensaje cliente: {}'.format(self.mensaje))
            time.sleep(30)

#------------------------------------------REPLY--------------------------------------------------
class ReplyServer(threading.Thread):

    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        self.mesas = []
        self.ip_sever = []
        self.cont = 0
    
    def run(self):
        while True:
            self.msj, self.ip_server[self.cont] = sock.recvfrom(4096)
            self.mesas.append(json.loads(self.msj))
            print('mensaje de repuesta {} desde el server {}'.format(mesas[self.cont],ip_server[self.cont]))
            self.cont = self.cont + 1

    def getMesas(self):
        return self.mesas

    def getIP_Sever(self):
        return self.ip_server

#--------------------------------------------MAIN-------------------------------------------------
if __name__ == '__main__':
    conection = ('127.255.255.255', 3001)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        req = RequestServer(conection, sock)
        #rep = ReplyServer(sock)
        req.start()
        #rep.start()
        req.join()
    except socket.error:
        print('error en el socket...')
        sys.exit()
