import sys
import socket
import json

class Jugador():

    def __init__(self, nombre, endpoint, socket):
        self.nombre = nombre
        self.fichas = []
        self.socketTCP = socket
    
    def enviarFicha(self, identificador):
        men = {
            'identificador': 'DOMINOCOMUNICACIONESI',
            'fichas': self.fichas
        }
        print(men)
        self.socketTCP.sendall(json.dumps(men).encode('utf-8'))
        

