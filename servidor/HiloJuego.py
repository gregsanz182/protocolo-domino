import sys
import json
import socket
import threading

class HiloJuego(threading.Thread):

    def __init__(self):
        super().__init__()
        self.TCPendpoint = ('localhost', 3001)
        self.jsonMulticast = {
            'identificador': 'DOMINOCOMUNICACIONESI',
            'multicast_ip': '254.569.122'
        }
        self.sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.sockTCP.bind(self.TCPendpoint)
        self.sockTCP.listen(1)

        while True:



