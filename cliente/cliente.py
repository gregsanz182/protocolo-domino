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

    def __init__(self, conection):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.conection = conection
        self.mensaje_json = {
            "identificador": "DOMINOCOMUNICACIONESI"
        }

    def run(self):
        while True:
            self.mensaje = json.dumps(self.mensaje_json).encode('utf-8')
            self.sock.sendto(self.mensaje, self.conection)
            print('mensaje cliente: {}'.format(self.mensaje))
            time.sleep(2)

#------------------------------------------REPLY--------------------------------------------------
class ReplyServer(threading.Thread):

    def __init__(self):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.mesas = []
        self.ip_server = []
    
    def run(self):
        while True:
            self.msj, self.direc = self.sock.recvfrom(4096)
            self.mesas.append(json.loads(self.msj).decode('utf-8'))
            self.ip_server.append(self.direc)
            print(self.mesas)
            print(self.ip_server)

    def getMesas(self):
        return self.mesas

    def getIP_Sever(self):
        return self.ip_server

#--------------------------------------------MAIN-------------------------------------------------
if __name__ == '__main__':
    conection = ('127.255.255.255',3001)
    try:
        req = RequestServer(conection)
        req.start()
        time.sleep(2)
        rep = ReplyServer()
        rep.start()
        req.join()
    except socket.error:
        print('error en el socket...')
        sys.exit()
