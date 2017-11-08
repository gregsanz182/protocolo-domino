import sys
import json
import socket
import threading

class hiloEscuchaTCP(threading.Thread):

    def __init__(self):
        self.TCPendpoint = ('localhost', 3001)