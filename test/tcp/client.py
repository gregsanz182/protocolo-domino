import socket
import sys
import json

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 2134)
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

        amount_received = 0
        amount_expected = len(message)
        cad = ''

        while amount_received < amount_expected:
            data = sock.recv(2024)
            amount_received += len(data)
            cad = cad+data.decode('utf-8')

        mem = json.loads(cad)
        print(mem)

    finally:
        print('Cerrando Socket')
        sock.close()
