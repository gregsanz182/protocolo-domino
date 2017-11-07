#
#   Cliente - Dominó
#

import socket
import json
import sys

class conection:
    ip
    port
    sock
    def __init__(self, UDP_IP, UDP_port):
        self.ip = UDP_IP
        self.port = UDP_port
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print('el Socket no se abrio correctamente...')
            sys.exit()
    def conect(self):
        self.mensaje = format(json.dump({"identificador": "DOMINOCOMUNICACIONES1"}))
        while true:
            sock.sendto(mensaje,(self.ip,self.port))