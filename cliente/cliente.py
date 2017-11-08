#
#   Cliente - Dominó
#

import socket
import json
import sys
import pthreading

class conection:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print('error en el socket...')
            sys.exit()

    def conect(self):
        self.mensaje_json = {
            "identificador": "DOMINOCOMUNICACIONES1"
        }
        self.mensaje = json.dumps(self.mensaje_json).encode('utf-8')
        while True:
            self.sock.sendto(self.mensaje, (self.ip, self.port))

if __name__ == '__main__':
    s = conection('localhost',3001)
    s.conect()