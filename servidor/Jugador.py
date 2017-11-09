import sys
import socket
import json

class Jugador():

    def __init__(self, nombre, idenJugador, endpoint, socket):
        self.nombre = nombre
        self.fichas = []
        self.socketTCP = socket
        self.idenJugador = idenJugador
    
    def enviarFicha(self, identificador):
        men = {
            'identificador': 'DOMINOCOMUNICACIONESI',
            'fichas': self.fichas
        }
        print(men)
        self.socketTCP.sendall(json.dumps(men).encode('utf-8'))
        
    def verificarFicha(self, ficha):
        for ficha in self.fichas:
            if ficha['entero_uno'] == ficha[0] and ficha['entero_dos'] == ficha[1]:
                return ficha
        return None
