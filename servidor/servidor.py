import sys
import socket
import json
from hiloDisponibilidad import hiloDisponibilidad

if __name__ == '__main__':

    disp = hiloDisponibilidad()

    disp.start()
    disp.join()


        