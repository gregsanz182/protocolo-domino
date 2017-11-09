import socket
import sys
import json

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('192.168.0.3', 3001)
    print('Conectandose a {} port {}'.format(*server_address))
    sock.connect(server_address)

    men = {
        'identificador': 'DOMINOCOMUNICACIONESI',
        'nombre_jugador': 'greg'
    }

    try:
        message = json.dumps(men).encode('utf-8')
        print('Enviando {!r}'.format(message))
        sock.sendall(message)

        data = sock.recv(4096)

        mem = json.loads(data)
        print(mem)
        while True:
            pass

    finally:
        print('Cerrando Socket')
        sock.close()
