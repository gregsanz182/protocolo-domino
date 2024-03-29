import sys
import socket
import json

class Jugador():

    def __init__(self, nombre, idenJugador, endpoint, socket):
        self.nombre = nombre
        self.fichas = []
        self.socketTCP = socket
        self.idenJugador = idenJugador
        self.puntos = 0
    
    def enviarFicha(self, identificador):
        men = {
            'identificador': identificador,
            'tipo': 2,
            'fichas': self.fichas
        }
        print(men)
        self.socketTCP.sendall(json.dumps(men).encode('utf-8'))
        return men
        
    def verificarFicha(self, tokenFicha):
        for ficha in self.fichas:
            if ficha['token'] == tokenFicha:
                return ficha
        return None

    def contarPintas(self):
        return sum([(ficha['entero_uno']+ficha['entero_dos']) for ficha in self.fichas])

    def disponibilidadPinta(self, pinta):
        for ficha in self.fichas:
            if pinta in [ficha['entero_uno'], ficha['entero_dos']]:
                return True
        return False

    def aumentarPuntos(self, suma):
        self.puntos += suma
        