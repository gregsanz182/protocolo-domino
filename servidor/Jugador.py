import sys
import socket
import json

class Jugador():

    def __init__(self, nombre, endpoint, socket):
        self.nombre = nombre
        self.fichas = []
        self.socketTCP = socket
    
    def enviarFicha(self):
        self.socketTCP.sendall(json.dumps(self.fichas).encode('utf-8'))
        

