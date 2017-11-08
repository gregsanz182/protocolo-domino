import sys
import socket

class Jugador():

    def __init__(self, nombre, endpoint, socket):
        self.nombre = nombre
        self.fichas = []
        self.socketTCP = socket
        
