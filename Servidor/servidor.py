import sys
import socket
import json
from HiloJuego import HiloJuego

if __name__ == '__main__':

    juego = HiloJuego()
    juego.start()
    juego.join()